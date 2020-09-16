"""New syntax test file"""

import time
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

from .command import run_command


def enable_network_connection(gateway_address: Optional[str]) -> [CompletedProcess]:
    path = Path()
    from sys import platform
    results = []
    if platform == "linux":
        # result = run_command("nmcli nm enable true", path)
        result = run_command("ip link set eth0 up", path)
        results.append(result)
        print(result.stdout)
        if gateway_address is not None:
            result = run_command(f"route add default gw {gateway_address}", path)
            results.append(result)
            print(result.stdout)
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
        # result = run_command("nmcli nm enable false", path)
        result = run_command("ip link set eth0 down", path)
        print(result.stdout)
    elif platform == "darwin":
        result = run_command("networksetup -setairportpower airport off", path)
    elif platform == "win32":
        assert False
    else:
        assert False
    time.sleep(5)
    return result


def get_gateway_ip_address() -> Optional[str]:
    path = Path()
    from sys import platform
    if platform == "linux":
        result = run_command("netstat -nr | awk '{print $2}' | head -n3 | tail -n1", path)
        print(result.stdout)
        return result.stdout.strip()
    elif platform == "darwin":
        return None
    elif platform == "win32":
        assert False
    else:
        assert False
