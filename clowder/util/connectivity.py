"""Network connectivity

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import socket
from functools import wraps

from clowder.error import *


def is_offline(host: str = '8.8.8.8', port: int = 53, timeout: int = 3) -> bool:
    """Returns True if offline, False otherwise

    Service: domain (DNS/TCP)

    .. note:: Implementation source https://stackoverflow.com/a/33117579

    :param str host: Host to check. Default is 8.8.8.8 (google-public-dns-a.google.com)
    :param int port: Port number. Default is 53/tcp
    :param int timeout: Seconds to wait until timeout
    :return: True, if offline
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True


def network_connection_required(func):
    """If no network connection, print offline message and exit

    :raise NetworkConnectionError:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if is_offline():
            raise NetworkConnectionError('No available internet connection')
        return func(*args, **kwargs)

    return wrapper
