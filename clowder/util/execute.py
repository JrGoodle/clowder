"""Subprocess execution utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union

import clowder.util.formatting as fmt
from clowder.console import CONSOLE


def execute_command(command: Union[str, List[str]], path: Path,
                    env: Optional[dict] = None, print_output: Optional[bool] = None) -> None:
    """Execute command via subprocess

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    :raise ClowderError:
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

    pipe = None if print_output else subprocess.PIPE

    try:
        subprocess.run(cmd, shell=True, env=cmd_env, cwd=str(path), stdout=pipe, stderr=pipe, check=True)
    except subprocess.CalledProcessError:
        CONSOLE.stderr(f"Failed to run command {fmt.command(cmd)}")
        raise


def execute_forall_command(command: Union[str, List[str]], path: Path, forall_env: dict) -> None:
    """Execute forall command with additional environment variables and display continuous output

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    :raise ClowderError:
    """

    execute_command(command, path, env=forall_env)
