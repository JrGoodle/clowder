"""New syntax test file"""

from typing import List

import os
import subprocess
from subprocess import CompletedProcess, STDOUT, PIPE
from pathlib import Path


class CommandResults:
    def __init__(self):
        self.completed_processes: List[CompletedProcess] = []


def run_command(command: str, path: Path, check: bool = False, clowder_debug: bool = True) -> CompletedProcess:
    print(f"TEST: {command}")
    cmd_env = os.environ.copy()
    if clowder_debug:
        cmd_env.update({"CLOWDER_DEBUG": "true"})
    else:
        cmd_env.pop('CLOWDER_DEBUG', None)
    # TODO: Replace universal_newlines with text when Python 3.6 support is dropped
    result = subprocess.run(command, cwd=path, shell=True, check=check,
                            stdout=PIPE, stderr=STDOUT, universal_newlines=True, env=cmd_env)
    print(result.stdout)
    return result
