# -*- coding: utf-8 -*-
"""Subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import subprocess
from typing import List, Optional, Union

from termcolor import colored

from clowder.error import ClowderError


def execute_command(command: Union[str, List[str]], path: str,
                    env: Optional[dict] = None, print_output: bool = True) -> None:
    """Execute command via subprocess

    :param Union[str, List[str]] command: Command to run
    :param str path: Path to set as ``cwd``
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
        subprocess.run(cmd, shell=True, env=cmd_env, cwd=path, stdout=pipe, stderr=pipe, check=True)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(colored('- Command interrupted', 'red'))
    except subprocess.CalledProcessError as err:
        raise ClowderError(colored('\n - Command failed', 'red') + str(err) + '\n')


def execute_forall_command(command: Union[str, List[str]], path: str, forall_env: dict, print_output: bool) -> None:
    """Execute forall command with additional environment variables and display continuous output

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output

    :raise ClowderError:
    """

    execute_command(command, path, env=forall_env, print_output=print_output)
