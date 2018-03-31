#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  default.py
#
#  Copyright 2017 Jelle Smet <development@smetj.net>
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
from gevent import monkey; monkey.patch_all()

from wishbone.actor import ActorConfig
from wishbone.utils.test import getter
from wishbone.event import Event

from wishbone_input_httpserver import HTTPServer
import requests
from os import unlink


SSL_KEY = '''
-----BEGIN PRIVATE KEY-----
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
40+kApPARNrA+X/0VZIHX2YMixTepw==
-----END PRIVATE KEY-----
'''

SSL_CERT = '''
-----BEGIN CERTIFICATE-----
MIIFWjCCA0KgAwIBAgIJAMBDn8/vv1zMMA0GCSqGSIb3DQEBCwUAMEIxCzAJBgNV
BAYTAlhYMRUwEwYDVQQHDAxEZWZhdWx0IENpdHkxHDAaBgNVBAoME0RlZmF1bHQg
Q29tcGFueSBMdGQwHhcNMTgwMTAzMDk1NTA3WhcNMTkwMTAzMDk1NTA3WjBCMQsw
CQYDVQQGEwJYWDEVMBMGA1UEBwwMRGVmYXVsdCBDaXR5MRwwGgYDVQQKDBNEZWZh
dWx0IENvbXBhbnkgTHRkMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA
liRqj745shAIhuxQXxsWrNYwjTDeI9P44yOUG9K89uWhHkk+pCTH+YYmXKbArpq6
T/VC8SqKT1BX2pl3h7u40uE4a8pLL4mTE8o07C4QzK2181D3ey7yAO/LTrOPG6FO
CdItcyNB9lCVFAJ0Z8vRSAEtFlUSR3S4QRIwxpiYNWkjBNdMp65+Ciy3fuf5p82M
YSkXE6yn2PpgkV8eLJ7nP+Tzh0UtoOp1dDp9F612efPSkSQm0KRdf5jYZ77QVLEn
HmgpImY1OSPDoevIurRlLB7b/RBo2GjEyJm5lh2vMyATOmXO9IBPasxj3VDjSIYH
JTYH7bun7n2VZJM/m7EIUtNO+ZOn0v3kn/1Ww7ko+PCHOMuPPK90H9c1Wpfd4rng
mmI7lPuuEviFTr9fOx1K/uhxnO7Q+m+MfvcDdZSlkXCclE0zZZYcFNuhv5akQj75
HrWxs/R8CkHMrHOz6AIjrttYIQiSnRqPvhrxrgbby72tOUkfGrrTt/F/fKgqof9C
+5rRTq4Re6GfvhZvE1hEkZQsrKs0DhMP1sYVyR48GZXj8ttGv1xQPFBEKQvchxec
pjsFePncP1wTQirBw+YO6SBC3fO0BYU04ykJxMCDFrmftyT3XB57d6HEzRiJ7MNk
MJV0W+a4XQgWJQteopNdA8XGDXv44BC2dUDA5q1eRaECAwEAAaNTMFEwHQYDVR0O
BBYEFHtkIUg/dkgBBznKxE/MWUj1pAwhMB8GA1UdIwQYMBaAFHtkIUg/dkgBBznK
xE/MWUj1pAwhMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggIBABnV
CxmFOu1aSn/EMUlTqqS8uWv0n5lcUt8slV030dyB/YLfi3dW1BKWNecrAb+0s2Fu
6ioXcU2JMcf8xXUm9aKGZuM/T6wlstkmSOCfhy/2gCgIK/FGKHg6qTX+PO5gAhHk
4Phr0SOwyz3lF7uBpe6HiEfKylB2Gd06FKmnX7GWtkuDzaO/kH8UuSHVBYs+pCGD
U5NHnLP2KwxvkN/ywY6m9CkgHcrM2+Wu5d/N+29rE/+GmRyXNGERJfbtHFZ+83IJ
7suO3e+GdLwoufHKCerbAE3xosgCDCnXkttzfGnTGGCeDxCGQlSAwdr7UOEOLlNi
4pML+NnX3yUHbrjBBjPAUUww7Q7zE79T+MXGDPIDEfQw+Q7XomCsZf31Dhz0jAuT
Ffl/aHAZKu3ka/BT8CKVOkeqkbrx4kQYdgx1vbbWvWTakHdCOqqh+g987OtUlTaD
CsvHF3MXsbcoOom42/OwJL64frhr+fjr8KYRQuI+Y2BFmtsDYR3+QT9CnvN3Fd5P
wV+Mkz9SIINchNOMb+gZbvYqeL/e9hH6guDxKA2Yra0TivcD8cDSekAMQludXQhH
aVymj8d9xbqftgNKOQ/lAPhuJ4LF3vAvHAiIPHPr5yMBRwFTTNq8Qx8Ph1+SJpJ+
vA3JtRgodsbaZ5RbIQk1SKeeuIqUXGUCrZmh37p6
-----END CERTIFICATE-----
'''


class TempFile(object):

    def __init__(self, filename, content):

        self.filename = filename
        with open(filename, "w") as f:
            f.write(content)

    def __enter__(self, *args, **kwargs):

        return self

    def __exit__(self, *args, **kwargs):

        unlink(self.filename)


def test_module_http_response_default():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283')
    http.stop()
    r.close()

    assert r.status_code == 200
    assert r.text.startswith("200 OK")


def test_module_http_native_events():

    from wishbone.componentmanager import ComponentManager

    decoder = ComponentManager().getComponentByName("wishbone.protocol.decode.json")()

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True, protocol=lambda: decoder.handler)

    http = HTTPServer(actor_config, native_events=True)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283', json=Event().dump())
    r.close()

    http.stop()
    assert r.status_code == 200


def test_module_http_native_events_bad():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config, native_events=True)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283', data="hello")
    r.close()

    http.stop()
    assert r.status_code == 400


def test_module_https_response_default():

    requests.packages.urllib3.disable_warnings()
    with open('/tmp/ssl.key', 'w') as f:
        f.write(SSL_KEY)

    with open('/tmp/ssl.cert', 'w') as f:
        f.write(SSL_CERT)

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config, ssl_key="/tmp/ssl.key", ssl_cert="/tmp/ssl.cert")

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('https://localhost:19283', verify=False)
    http.stop()
    r.close()

    assert r.status_code == 200
    assert r.text.startswith("200 OK")

    unlink("/tmp/ssl.key")
    unlink("/tmp/ssl.cert")


def test_module_http_response_new_queue():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config)

    http.pool.createQueue("outbox")
    http.pool.createQueue("abc")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/abc')
    http.stop()
    r.close()

    assert r.status_code == 200
    assert r.text.startswith("200 OK")


def test_module_http_response_non_existing():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/abc')
    http.stop()
    r.close()

    assert r.status_code == 404


def test_module_http_response_user_auth_ok():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": ["test"], "tokens": [], "response": "OK {{uuid}}", "urldecoded_field": None}},
        htpasswd={"test": "$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/outbox', auth=("test", "test"))
    http.stop()
    r.close()

    assert r.status_code == 200


def test_module_http_response_user_auth_denied():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": ["test"], "tokens": [], "response": "OK {{uuid}}", "urldecoded_field": None}},
        htpasswd={"test": "$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/outbox', auth=("test", "wrong"))
    http.stop()
    r.close()

    assert r.status_code == 401


def test_module_http_response_user_auth_bad_header1():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": ["test"], "tokens": [], "response": "OK {{uuid}}", "urldecoded_field": None}},
        htpasswd={"test": "$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/outbox', headers={"Authorization": "bad test"})
    http.stop()
    r.close()

    assert r.status_code == 400


def test_module_http_response_token_auth_ok():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": ["abc"], "response": "OK {{uuid}}", "urldecoded_field": None}}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/outbox', headers={"Authorization": "Token abc"})
    http.stop()
    r.close()

    assert r.status_code == 200


def test_module_http_response_token_auth_denied():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": ["abc"], "response": "OK {{uuid}}", "urldecoded_field": None}}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283/outbox', headers={"Authorization": "Token abcd"})
    http.stop()
    r.close()

    assert r.status_code == 403


def test_module_http_response_format():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": [], "response": "12345", "urldecoded_field": None}},
        htpasswd={}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283')
    http.stop()
    r.close()

    assert r.status_code == 200
    assert r.text == "12345"


def test_module_http_response_format_extra_params():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": [], "response": "12345 {{tmp.http.params.one}}", "urldecoded_field": None}},
        htpasswd={}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.get('http://localhost:19283?one=1')
    http.stop()
    r.close()

    assert r.status_code == 200
    assert r.text == "12345 1"


def test_module_http_invalid_resource():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    try:
        HTTPServer(
            actor_config,
            resource={".*": {"xusers": [], "tokens": [], "response": "12345 {{tmp.http.params.one}}", "urldecoded_field": None}},
            htpasswd={}
        )
    except Exception:
        assert True
    else:
        False


def test_module_http_default_submit_event():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283/outbox', data="hello")
    r.close()

    assert getter(http.pool.queue.outbox).get() == "hello"
    http.stop()


def test_module_http_default_submit_event_outbox():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(actor_config)

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283', data="hello")
    r.close()

    assert getter(http.pool.queue.outbox).get() == "hello"
    http.stop()


def test_module_http_response_user_auth_load_file():

    with TempFile("/tmp/htpasswd", "test:$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"):

        actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
        http = HTTPServer(
            actor_config,
            resource={".*": {"users": ["test"], "tokens": [], "response": "OK {{uuid}}", "urldecoded_field": None}},
        )

        http.pool.createQueue("outbox")
        http.pool.queue.outbox.disableFallThrough()
        http.pool.queue._htpasswd.disableFallThrough()
        http.pool.queue._resource.disableFallThrough()
        http.start()
        http.pool.queue._htpasswd.put(Event({"path": "/tmp/htpasswd", "inotify_type": "WISHBONE_INIT"}))
        r = requests.get('http://localhost:19283/outbox', auth=("test", "test"))
        http.stop()
        r.close()

        assert r.status_code == 200


def test_module_http_response_user_auth_order():

    with TempFile("/tmp/htpasswd", "test:$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"):

        actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
        http = HTTPServer(
            actor_config,
            resource={".*": {"users": ["test", "test2"], "tokens": [], "response": "OK {{uuid}}", "urldecoded_field": None}},
            htpasswd={"test": "$apr1$abc", "test2": "$apr1$rUKXjcuX$hqdIeoE2Q1Z/GMFhYsNO91"}
        )

        http.pool.createQueue("outbox")
        http.pool.queue.outbox.disableFallThrough()
        http.pool.queue._htpasswd.disableFallThrough()
        http.pool.queue._resource.disableFallThrough()
        http.start()
        http.pool.queue._htpasswd.put(Event({"path": "/tmp/htpasswd", "inotify_type": "WISHBONE_INIT"}))

        r = requests.get('http://localhost:19283/outbox', auth=("test", "test"))
        assert r.status_code == 200

        r = requests.get('http://localhost:19283/outbox', auth=("test2", "test"))
        assert r.status_code == 200

        http.stop()
        r.close()


def test_module_http_response_default_so_reuseport():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)

    http1 = HTTPServer(
        actor_config,
        so_reuseport=True,
        resource={".*": {"users": [], "tokens": [], "response": "server1", "urldecoded_field": None}},
    )
    http1.pool.createQueue("outbox")
    http1.pool.queue.outbox.disableFallThrough()
    http1.start()

    http2 = HTTPServer(
        actor_config,
        so_reuseport=True,
        resource={".*": {"users": [], "tokens": [], "response": "server2", "urldecoded_field": None}},
    )
    http2.pool.createQueue("outbox")
    http2.pool.queue.outbox.disableFallThrough()
    http2.start()

    result = []

    # Check whether we actually hit both instances
    # In 10 times that should really be the case
    for _ in range(10):
        r = requests.get('http://localhost:19283')
        assert r.status_code == 200
        result.append(r.text)
    http2.stop()
    http1.stop()

    assert ["server1", "server2"] == sorted(set(result))


def test_module_http_default_submit_urlencoded():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": [], "response": "hello", "urldecoded_field": "payload"}}
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283', data={"payload": "hello there"})
    r.close()

    assert getter(http.pool.queue.outbox).get() == "hello there"
    http.stop()


def test_module_http_default_submit_urlencoded_max_bytes():

    actor_config = ActorConfig('http', 100, 1, {}, "", disable_exception_handling=True)
    http = HTTPServer(
        actor_config,
        resource={".*": {"users": [], "tokens": [], "response": "hello", "urldecoded_field": "payload"}},
        max_bytes=5
    )

    http.pool.createQueue("outbox")
    http.pool.queue.outbox.disableFallThrough()
    http.start()

    r = requests.post('http://localhost:19283', data={"payload": "hello there"})
    r.close()

    assert r.status_code == 406
