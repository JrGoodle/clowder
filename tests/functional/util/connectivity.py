"""New syntax test file"""

import time
from pathlib import Path
from subprocess import CompletedProcess

from .command import run_command


def enable_network_connection() -> CompletedProcess:
    path = Path()
    from sys import platform
    if platform == "linux":
        result = run_command("ip link set eth0 up", path)
    elif platform == "darwin":
        result = run_command("networksetup -setairportpower airport on", path)
    elif platform == "win32":
        assert False
    else:
        assert False
    time.sleep(5)
    return result


def disable_network_connection() -> CompletedProcess:
    path = Path()
    from sys import platform
    if platform == "linux":
        result = run_command("ip link set eth0 down", path)
    elif platform == "darwin":
        result = run_command("networksetup -setairportpower airport off", path)
    elif platform == "win32":
        assert False
    else:
        assert False
    time.sleep(5)
    return result
