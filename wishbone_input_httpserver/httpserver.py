#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  falconserver.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gevent import monkey
monkey.patch_all()
from wishbone.module import InputModule
from wishbone.event import Event
from wishbone.protocol.decode.plain import Plain
from .app import FalconServer
import re
from wishbone.utils import StructuredDataFile
from itertools import chain


class HTTPServer(InputModule):

    '''**Receive events over HTTP.**

    An HTTP server mapping URL endpoints to queues to which events can be
    submitted.

    Mapping queues to endpoints::

        Connecting queues to this module automatically maps them to the equivalent
        URL endpoint.

        The "/" endpoint is by default mapped to the <outbox> queue.


    Authentication and authorization behavior::

        - The htpasswd and resource file content override any duplicate entries
          defined in ``resource`` and ``htpasswd``.
        - Htpasswd is evaluated first before token validation.
        - You cannot define htpasswd and token authentication on the same
          resource definition.

    Available meta data::

        Each event has some meta associated stored in tmp.<instance_name>

        {
        "env": {
            "content_length": "288014336",
            "content_type": "application/x-www-form-urlencoded",
            "gateway_interface": "CGI/1.1",
            "http_accept": "*/*",
            "http_expect": "100-continue",
            "http_host": "localhost:19283",
            "http_user_agent": "curl/7.53.1",
            "path_info": "/outbox",
            "query_string": "one=1&two=2",
            "remote_addr": "127.0.0.1",
            "remote_port": "60924",
            "request_method": "POST",
            "script_name": "",
            "server_name": "localhost",
            "server_port": "19283",
            "server_protocol": "HTTP/1.1",
            "server_software": "gevent/1.2 Python/3.6",
            "wsgi.url_scheme": "http"
        },
        "headers": {
            "accept": "*/*",
            "content-length": "288014336",
            "content-type": "application/x-www-form-urlencoded",
            "expect": "100-continue",
            "host": "localhost:19283",
            "user-agent": "curl/7.53.1"
        },
        "params": {
            "one": "1",
            "two": "2"
        }
        }

    Parameters::

        - address(str)("0.0.0.0")
           |  The address to bind to.

        - port(int)(19283)
           |  The port to bind to.

        - ssl_key(str)(None)
           |  When SSL is required, the location of the ssl_key to use.

        - ssl_cert(str)(None)
           |  When SSL is required, the location of the ssl_cert to use.

        - ssl_cacerts(str)(None)
            |  When SSL is required, the location of the ca certs to use.

        - poolsize(int)(1000)
            |  The connection pool size.

        - so_reuseport(bool)(False)
            |  Enables socket option SO_REUSEPORT.
            |  See https://lwn.net/Articles/542629/
            |  Required when running multiple Wishbone instances.

        - resource(dict)({".*": {"users:": [], "tokens": [], "response": "OK {{uuid}}"}})
            |  Contains all endpoint authorization related config.
            |  The moment at least 1 user or token is defined the
            |  queue/endpoint needs authentication.

        - htpasswd(dict)({})
            |  The htpasswd username and password data.

    Queues::

        Queue 'read_htpasswd' and 'read_tokens' are reserved queue names.
        These queues expect events containing the filename of the htpasswd or
        tokens file respectively. Typically the
        `wishbone.module.input.inotify` module is used for this.

        - outbox
           |  Incoming events submitted to /

        - _resource
           |  Triggers the resource file to be reloaded.
           |  The event payload should contain the absolute filename to load

        - _htpasswd
           |  Triggers the htpasswd file to be reloaded.
           |  The event payload should contain the absolute filename to load

        - <queue_name>
           |  Incoming events submitted to /<queue_name>
    '''

    RESOURCE_SCHEMA = {
        "type": "object",
        "patternProperties": {
                ".*": {
                    "type": "object",
                    "properties": {
                        "users": {
                            "type": "array"
                        },
                        "tokens": {
                            "type": "array"
                        },
                        "response": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "users",
                        "tokens",
                        "response"
                    ]
                }
        }
    }

    def __init__(self, actor_config,
                 address="0.0.0.0", port=19283, poolsize=1000, so_reuseport=False,
                 ssl_key=None, ssl_cert=None, ssl_cacerts=None,
                 resource={".*": {"users": [], "tokens": [], "response": "OK {{uuid}}"}}, htpasswd={}):
        InputModule.__init__(self, actor_config)

        self.pool.createSystemQueue("_htpasswd")
        self.registerConsumer(self.readHtpasswdFile, "_htpasswd")

        self.pool.createSystemQueue("_resource")
        self.registerConsumer(self.readResourceFile, "_resource")

        self.decode = Plain().handler

        self.htpasswd_file = StructuredDataFile(default={}, expect_json=False, expect_yaml=False)
        self.resource_file = StructuredDataFile(schema=self.RESOURCE_SCHEMA, default={}, expect_json=False, expect_kv=False)

    def preHook(self):
        self.server = FalconServer(
            address=self.kwargs.address,
            port=self.kwargs.port,
            ssl_key=self.kwargs.ssl_key,
            ssl_cert=self.kwargs.ssl_cert,
            ssl_cacerts=self.kwargs.ssl_cacerts,
            poolsize=self.kwargs.poolsize,
            so_reuseport=self.kwargs.so_reuseport,
            wishbone_event_callback=self.processEvent,
            wishbone_logger=self.logging,
            wishbone_decoder=self.decode,
            wishbone_queues=self.pool.listQueues,
            callback_authorize_user=self.authorizeUser,
            callback_authorize_token=self.authorizeToken,
            callback_get_password_hash=self.getPasswordHash,
            callback_requires_authentication=self.requiresAuthentication
        )

        self.server.start()

    def authorizeToken(self, token, endpoint):
        '''
        Validates whether ``token`` is allowed to submit to ``endpoint``

        Args:
            token (str): The token to validate
            endpoint (str): The endpoint (queue name) to validate ``token`` against.

        Returns:
            bool: True when ``token`` is authorized otherwise False
        '''

        for item in chain(self.resource_file.dumpItems(), [self.kwargs.resource]):
            for key, value in item.items():
                if re.match(key, endpoint):
                    if token in value["tokens"]:
                        return True
                    else:
                        return False

        # Not a single endpoint selector matched therefor no auth required.
        return True

    def authorizeUser(self, username, endpoint):
        '''
        Validates whether ``username`` is allowed to submit to ``endpoint``

        Args:
            username (str): The username to validate
            endpoint (str): The endpoint (queue name) to validate ``username`` against.

        Returns:
            bool: True when ``username`` is authorized otherwise False
        '''

        for item in chain(self.resource_file.dumpItems(), [self.kwargs.resource]):
            for key, value in item.items():
                if re.match(key, endpoint):
                    if username in value["users"]:
                        True
                    else:
                        return False

        # Not a single endpoint selector matched therefor no auth required.
        return True

    def getPasswordHash(self, username):
        '''
        Returns the password hash of ``user``

        Args:
            username (str): The username

        Returns:
            str: The password hash of ``user``
        '''

        for item in chain(self.htpasswd_file.dumpItems(), [self.kwargs.htpasswd]):
            if username in item:
                return item[username]

        return None

    def getResponse(self, event, queue):
        '''
        Selects the reponse associated to the endpoint defined by the user in self.kwargs.response
        '''

        for key, value in event.kwargs.resource.items():
            if re.match(key, queue):
                return value["response"]

    def requiresAuthentication(self, endpoint):
        '''
        Checks whether ``endpoint`` requires user or token authentication.

        Args:
            endpoint (str): The endpoint to validate

        Returns:
            bool: True if endpoint requires user auth False if not.
        '''

        for item in chain(self.resource_file.dumpItems(), [self.kwargs.resource]):
            for key, value in item.items():
                if re.match(key, endpoint):
                    if len(self.kwargs.resource[key]["users"]) > 0 or len(self.kwargs.resource[key]["tokens"]) > 0:
                        return True
                    else:
                        return False

    def postHook(self):

        self.server.stop()

    def processEvent(self, data, meta, queue):
        '''
        The callback executed for each Wishbone event to be created out of a
        single http request.
        '''

        e = Event(data)
        e.set(meta, 'tmp.%s' % (self.name))
        e.renderKwargs(self.kwargs_template)
        self.submit(e, queue)

        return self.getResponse(e, queue)

    def readHtpasswdFile(self, event):
        '''
        Reads the htpasswd file.
        Expects the incoming event to contain a payload like:

        ``{"path": "/tmp/test", "inotify_type": "IN_ACCESS"}``

        Typically the ``wishbone.module.input.inotify`` modules
        provides these.
        '''

        self.htpasswd_file.load(
            event.get(
                "data.path"
            )
        )

    def readResourceFile(self, event):
        '''
        Reads the resource file.
        Expects the incoming event to contain a payload like:

        ``{"path": "/tmp/test", "inotify_type": "IN_ACCESS"}``

        Typically the ``wishbone.module.input.inotify`` modules
        provides these.
        '''
        # IN_CLOSE_WRITE
        # WISHBONE_INIT

        self.resource_file.load(
            event.get(
                "data.path"
            )
        )
