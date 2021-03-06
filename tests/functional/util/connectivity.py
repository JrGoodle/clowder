"""New syntax test file"""

from pathlib import Path
from subprocess import CompletedProcess
from time import sleep
from typing import Optional

from .command import run_command


def enable_network_connection(gateway_address: Optional[str]) -> [CompletedProcess]:
    path = Path()
    from sys import platform
    results = []
    if platform == "linux":
        result = run_command("ip link set eth0 up", path)
        results.append(result)
        if gateway_address is not None:
            result = run_command(f"route add default gw {gateway_address}", path)
            results.append(result)
    elif platform == "darwin":
        result = run_command("networksetup -setairportpower airport on", path)
        sleep(2)
    elif platform == "win32":
        assert False
    else:
        assert False
    return result


def disable_network_connection() -> CompletedProcess:
    path = Path()
    from sys import platform
    if platform == "linux":
        result = run_command("ip link set eth0 down", path)
    elif platform == "darwin":
        result = run_command("networksetup -setairportpower airport off", path)
        sleep(1)
    elif platform == "win32":
        assert False
    else:
        assert False
    return result


def get_gateway_ip_address() -> Optional[str]:
    path = Path()
    from sys import platform
    if platform == "linux":
        result = run_command("netstat -nr | awk '{print $2}' | head -n3 | tail -n1", path)
        return result.stdout.strip()
    elif platform == "darwin":
        return None
    elif platform == "win32":
        assert False
    else:
        assert False
