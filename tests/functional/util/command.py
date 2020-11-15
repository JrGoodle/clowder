"""New syntax test file"""

from typing import List

import os
import re
import subprocess
from subprocess import CompletedProcess, STDOUT, PIPE
from pathlib import Path


class CommandResults:
    def __init__(self):
        self.completed_processes: List[CompletedProcess] = []


def run_command(command: str, path: Path) -> CompletedProcess:
    print(f"TEST: {command}")
    cmd_env = os.environ.copy()
    cmd_env.update({"CLOWDER_DEBUG": "true"})

    processed_cmd = _process_clowder_commands(command)

    # TODO: Replace universal_newlines with text when Python 3.6 support is dropped
    print(processed_cmd)
    result = subprocess.run(processed_cmd, cwd=path, shell=True,
                            stdout=PIPE, stderr=STDOUT, universal_newlines=True, env=cmd_env)
    print(result.stdout)
    return result


def _process_clowder_commands(command: str) -> str:

    pattern = r'^(clowder(.+?))'
    replace = r'python -m clowder.clowder_app '
    output = re.sub(pattern, replace, command)

    return output
