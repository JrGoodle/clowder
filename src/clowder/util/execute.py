# -*- coding: utf-8 -*-
"""Subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool
from typing import List, Optional, Union

from termcolor import colored

from clowder.error.clowder_error import ClowderError


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def subprocess_exit_handler(process: subprocess.Popen) -> None:
    """terminate subprocess

    :param Popen process: Popen subprocess instance
    """

    try:
        process.terminate()
    except Exception as err:
        del err


def execute_subprocess_command(command: Union[str, List[str]], path: str, shell: bool = True,
                               env: Optional[dict] = None, stdout: Optional[int] = None,
                               stderr: Optional[int] = None) -> None:
    """Execute subprocess command

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``
    :param bool shell: Whether to execute subprocess as ``shell``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param Optional[int] stdout: Value to set as ``stdout``
    :param Optional[int] stderr: Value to set as ``stderr``

    :raise ClowderError:
    """

    if isinstance(command, list):
        cmd = ' '.join(command)
    else:
        cmd = command

    try:
        process = subprocess.Popen(cmd, shell=shell, env=env, cwd=path,
                                   stdout=stdout, stderr=stderr)
        atexit.register(subprocess_exit_handler, process)
        process.communicate()
        if process.returncode != 0:
            raise ClowderError
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as err:
        raise ClowderError(err)


def execute_command(command: Union[str, List[str]], path: str, shell: bool = True,
                    env: Optional[dict] = None, print_output: bool = True) -> int:
    """Execute command via thread

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``
    :param bool shell: Whether to execute subprocess as ``shell``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output

    :return: Command return code
    :rtype: int
    :raise ClowderError:
    """

    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    if print_output:
        pipe = None
    else:
        pipe = subprocess.PIPE

    pool = ThreadPool()

    try:
        result = pool.apply(execute_subprocess_command,
                            args=(command, path),
                            kwds={'shell': shell, 'env': cmd_env, 'stdout': pipe, 'stderr': pipe})
        pool.close()
        pool.join()
        return result
    except (KeyboardInterrupt, SystemExit):
        if pool:
            pool.close()
            pool.terminate()
        raise ClowderError(colored('- Command interrupted', 'red'))
    except Exception as err:
        if pool:
            pool.close()
            pool.terminate()
        raise ClowderError(colored('\n - Command failed', 'red') + str(err) + '\n')


def execute_forall_command(command: Union[str, List[str]], path: str, forall_env: dict, print_output: bool) -> int:
    """Execute forall command with additional environment variables and display continuous output

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    :return: Command return code
    :rtype: int
    """

    return execute_command(command, path, env=forall_env, print_output=print_output)
