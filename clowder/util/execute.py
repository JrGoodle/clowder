# -*- coding: utf-8 -*-
"""Subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG


def execute_command(command: Union[str, List[str]], path: Path,
                    env: Optional[dict] = None, print_output: bool = True) -> None:
    """Execute command via subprocess

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    :raise ClowderError:
    """

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
    except subprocess.CalledProcessError as err:
        LOG_DEBUG('Subprocess run failed', err)
        raise ClowderError(ClowderErrorType.FAILED_EXECUTE_COMMAND,
                           fmt.error_command_failed(cmd),
                           error=err,
                           exit_code=err.returncode)


def execute_forall_command(command: Union[str, List[str]], path: Path, forall_env: dict, print_output: bool) -> None:
    """Execute forall command with additional environment variables and display continuous output

    :param Union[str, List[str]] command: Command to run
    :param Path path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    :raise ClowderError:
    """

    execute_command(command, path, env=forall_env, print_output=print_output)
