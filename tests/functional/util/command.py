"""New syntax test file"""

import re
from pathlib import Path
from subprocess import CompletedProcess
from typing import List

import pygoodle.command as cmd
from pygoodle.console import CONSOLE


class CommandResults:
    def __init__(self):
        self.completed_processes: List[CompletedProcess] = []


def run_command(command: str, cwd: Path, check: bool = False) -> CompletedProcess:
    env = {"DEBUG": "true"}
    processed_command = _process_clowder_commands(command)
    result = cmd.run(processed_command, cwd=cwd, check=check, print_output=False, print_command=True, env=env)

    output = result.stdout.strip()
    if output:
        print(output)
    CONSOLE.stdout(f'Return code: {result.returncode}')
    if check:
        assert result.returncode == 0
    return result


def _process_clowder_commands(command: str) -> str:

    pattern = r'^(clowder(.+?))'
    replace = r'python3 -m clowder.app '
    output = re.sub(pattern, replace, command)

    return output
