"""Subprocess execution utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
import subprocess
from subprocess import CompletedProcess
from pathlib import Path
from typing import List, Optional, Union

from clowder.console import CONSOLE


def execute_command(command: Union[str, List[str]], path: Path,
                    env: Optional[dict] = None, print_output: Optional[bool] = None) -> CompletedProcess:
    """Execute command via subprocess

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    """

    if print_output is None:
        print_output = CONSOLE.print_output

    if isinstance(command, list):
        cmd = ' '.join(command)
    else:
        cmd = command

    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    stdout = None if print_output else subprocess.PIPE
    stderr = None if print_output else subprocess.STDOUT

    result = subprocess.run(cmd, shell=True, env=cmd_env, cwd=str(path),
                            stdout=stdout, stderr=stderr, universal_newlines=True, check=True)
    return result


def execute_forall_command(command: Union[str, List[str]], path: Path, forall_env: dict) -> None:
    """Execute forall command with additional environment variables and display continuous output

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    """

    execute_command(command, path, env=forall_env)
