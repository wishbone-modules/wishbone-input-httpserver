::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =========================
    wishbone.input.httpserver
    =========================

    Version: 1.0.0

    Receive events over HTTP.
    -------------------------


        Creates an HTTP server to which events can be submitted.


        Parameters:

            - address(str)("0.0.0.0")
               |  The address to bind to.

            - port(int)(19283)
               |  The port to bind to.

            - keyfile(str)(None)
               |  When SSL is required, the location of the keyfile to use.

            - certfile(str)(None)
               |  When SSL is required, the location of the certfile to use.

            - ca_certs(str)(None)
                |  When SSL is required, the location of the ca certs to use.

            - delimiter(str)(None)
               |  The delimiter which separates multiple
               |  messages in a stream of data.

            - poolsize(int)(1000)
                |  The connection pool size.

            - so_reuseport(bool)(False)
                |  Enables socket option SO_REUSEPORT.
                |  See https://lwn.net/Articles/542629/
                |  Required when running multiple Wishbone instances.

            - response(str)("ok")*
                |  The value of the response.  Can be a lookup function.
                |  This value is also stored under @tmp.<module>.response


        Queues:

            - outbox
               |  Incoming events submitted to /.


        When more queues are connected to this module instance, they are
        automatically mapped to the URL resource.

        For example http://localhost:10080/fubar is mapped to the <fubar> queue.
        The root resource "/" is mapped the <outbox> queue.
