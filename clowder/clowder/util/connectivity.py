# -*- coding: utf-8 -*-
"""Network connectivity

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


import socket
import sys


def is_offline(host='8.8.8.8', port=53, timeout=3):
    """Returns True if offline, False otherwise

    Service: domain (DNS/TCP)

    .. note:: Implementation source https://stackoverflow.com/a/33117579

    :param str host: Host to check. Default is 8.8.8.8 (google-public-dns-a.google.com)
    :param int port: Port number. Default is 53/tcp
    :param int timeout: Seconds to wait until timeout
    :return: True, if offline
    :rtype: bool
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
