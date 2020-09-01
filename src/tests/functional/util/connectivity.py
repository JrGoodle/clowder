"""New syntax test file"""

from pathlib import Path
from subprocess import CompletedProcess

from .command import run_command


def enable_network_connection() -> CompletedProcess:
    path = Path()
    from sys import platform
    if platform == "linux":
        return run_command("nmcli nm enable true", path)
    elif platform == "darwin":
        return run_command("networksetup -setairportpower airport on", path)
    elif platform == "win32":
        assert False


def disable_network_connection() -> CompletedProcess:
    path = Path()
    from sys import platform
    if platform == "linux":
        return run_command("nmcli nm enable false", path)
    elif platform == "darwin":
        return run_command("networksetup -setairportpower airport off", path)
    elif platform == "win32":
        assert False
