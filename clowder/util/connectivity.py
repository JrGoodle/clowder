# -*- coding: utf-8 -*-
"""Network connectivity

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import socket
from functools import wraps

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType


def is_offline(host: str = '8.8.8.8', port: int = 53, timeout: int = 3) -> bool:
    """Returns True if offline, False otherwise

    Service: domain (DNS/TCP)

    .. note:: Implementation source https://stackoverflow.com/a/33117579

    :param str host: Host to check. Default is 8.8.8.8 (google-public-dns-a.google.com)
    :param int port: Port number. Default is 53/tcp
    :param int timeout: Seconds to wait until timeout
    :return: True, if offline
    :rtype: bool
    :raise ClowderError:
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True


def network_connection_required(func):
    """If no network connection, print offline message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper

        :raise ClowderError:
        """

        if is_offline():
            raise ClowderError(ClowderErrorType.OFFLINE, fmt.error_offline())
        return func(*args, **kwargs)

    return wrapper
