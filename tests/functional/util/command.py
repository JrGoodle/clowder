"""New syntax test file"""

from typing import List

import os
import re
import subprocess
from subprocess import CompletedProcess, STDOUT, PIPE
from pathlib import Path

from pygoodle.console import CONSOLE
from pygoodle.format import Format


class CommandResults:
    def __init__(self):
        self.completed_processes: List[CompletedProcess] = []


def run_command(command: str, path: Path, check: bool = False) -> CompletedProcess:
    cmd_env = os.environ.copy()
    cmd_env.update({"CLOWDER_DEBUG": "true"})
    processed_cmd = _process_clowder_commands(command)
    CONSOLE.stdout(Format.bold(f'> {processed_cmd}'))

    # TODO: Replace universal_newlines with text when Python 3.6 support is dropped
    result = subprocess.run(processed_cmd, cwd=path, shell=True, stdout=PIPE, stderr=STDOUT,
                            universal_newlines=True, env=cmd_env)

    output = result.stdout.strip()
    if output:
        print(output)
    CONSOLE.stdout(f'Return code: {result.returncode}')
    if check:
        assert result.returncode == 0
    return result


def _process_clowder_commands(command: str) -> str:

    pattern = r'^(clowder(.+?))'
    replace = r'python -m clowder.app '
    output = re.sub(pattern, replace, command)

    return output
