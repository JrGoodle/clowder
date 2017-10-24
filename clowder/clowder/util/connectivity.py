"""Network connectivity"""


import socket
import sys


def is_offline(host='8.8.8.8', port=53, timeout=3):
    """
    Returns True if offline, False otherwise
    Source: https://stackoverflow.com/a/33117579
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
