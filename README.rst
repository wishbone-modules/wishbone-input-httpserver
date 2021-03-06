::
              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|


    ========================================
    wishbone_contrib.module.input.httpserver
    ========================================

    Version: 3.0.8

    Receive events over HTTP.
    -------------------------

        **Receive events over HTTP.**

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
            - Loading multiple htpasswd and resource files is supported.  The
              order of loading determines the priority.

        Htpasswd and resource file loading behavior::

            - Events submitted to queue '_htpasswd' should have the event payload
              generated by wishbone.module.input.inotify.
            - Events submitted to queue '_resource' should have the event payload
              generated by wishbone.module.input.inotify.
            - Files are removed from cache using ``IN_DELETE_SELF`` events.
            - Files are loaded/updated to cache using ``WISHBONE_INIT`` and
              ``IN_CLOSE_WRITE`` events.

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

            - destination(str)("data")
               |  The event field to store incoming data.

            - htpasswd(dict)({})
                |  The htpasswd username and password data.

            - native_events(bool)(False)
               |  Whether to expect Wishbone native events or not.

            - poolsize(int)(1000)
                |  The connection pool size.

            - port(int)(19283)
               |  The port to bind to.

            - resource(dict)({".*": {"users:": [], "tokens": [], "response": "200 OK. {{uuid}}", "urldecoded_field": null}})
                |  Contains all endpoint authorization related config.
                |  The moment at least 1 user or token is defined the
                |  queue/endpoint needs authentication.

            - so_reuseport(bool)(False)
                |  Enables socket option SO_REUSEPORT.
                |  See https://lwn.net/Articles/542629/
                |  Required when running multiple Wishbone instances.

            - ssl_cacerts(str)(None)
                |  When SSL is required, the location of the ca certs to use.

            - ssl_cert(str)(None)
               |  When SSL is required, the location of the ssl_cert to use.

            - ssl_key(str)(None)
               |  When SSL is required, the location of the ssl_key to use.

            - max_bytes(int)(16777216)
                |  The maximum amount of bytes the client can send to the endpoint
                |  when the expected content is application/x-www-form-urlencoded.
                |  Keep in mind that the configured decoder also has a max number
                |  of bytes defined.

        Queues::

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

