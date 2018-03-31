#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  data_extractor.py
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

import falcon
import re
from urllib.parse import parse_qs
import urllib.parse
from wishbone.error import ProtocolError, InvalidData


class DataExtractor(object):
    '''
    A Falcon middleware which extracts and decodes the data out of the
    incoming request.
    '''

    def __init__(self, get_decoder, urldecoded_fields):

        self.getDecoder = get_decoder
        self.urldecoded_fields = urldecoded_fields

    def process_request(self, req, resp):

        if resp.status != "200 OK":
            return

        payload = None
        decoder = self.getDecoder()
        req.event_payloads = []

        # First check if we need to handle application/x-www-form-urlencoded
        ####################################################################
        for queue, field in self.urldecoded_fields.items():
            if re.match(queue, field):
                if req.method in ["POST", "PUT"]:
                    if req.content_type.lower() == "application/x-www-form-urlencoded":
                        payload = "\n".join([item.decode("utf-8") for item in req.stream.readlines()])
                        payload = urllib.parse.unquote(payload)
                        payload = parse_qs(payload)[field][-1]

        if payload is None:
            data_to_encode = req.stream
        else:
            data_to_encode = payload

        try:
            for chunk in [data_to_encode, None]:
                for item in decoder(chunk):
                    req.event_payloads.append(item)
        except ProtocolError as err:
            resp.status = falcon.HTTP_406
            resp.body = "406 Not Acceptable. There was an error processing your request. Reason: ProtocolDecodeError %s" % str(err)
        except InvalidData as err:
            resp.status = falcon.HTTP_400
            resp.body = "400 Bad Request. Unsupported event format. Reason: %s" % (err)
