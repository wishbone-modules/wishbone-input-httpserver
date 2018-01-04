::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|


    ========================================
    wishbone_contrib.module.input.httpserver
    ========================================

    Version: 3.0.0

    Receive events over HTTP.
    -------------------------
    **Receive events over HTTP.**

        An HTTP server mapping URL endpoints to queues to which events can be
        submitted.

        Mapping queues to endpoints:
        ---------------------------

        Connecting queues to this module automatically maps them to the equivalent
        URL endpoint.

        The "/" endpoint is by default mapped to the <outbox> queue.

        Available meta data:
        --------------------

        Each event has some meta associated stored in tmp.<instance_name>:

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

        Misc Behavior:
        --------------

        The htpasswd and resource file will have priority over what has been
        defined by ``htpasswd`` and ``resource`` parameter.


        Parameters:

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

        Queues:

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

