# -*- coding: utf-8 -*-
"""Subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool

from termcolor import cprint


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def subprocess_exit_handler(process):
    """terminate subprocess

    :param Popen process: Popen subprocess instance
    """

    try:
        process.terminate()
    except Exception as err:
        del err


def execute_subprocess_command(command, path, **kwargs):
    """Execute subprocess command

    :param command: Command to run. Can be str or list(str)
    :param str path: Path to set as ``cwd``

    Keyword Args:
        shell (bool): Whether to execute subprocess as ``shell``. Defaults to True
        env (dict): Enviroment to set as ``env``
        stdout (int): Value to set as ``stdout``
        stderr (int): Value to set as ``stderr``

    :return: Subprocess return code
    :rtype: int
    """

    shell = kwargs.get('shell', True)
    env = kwargs.get('env', None)
    stdout = kwargs.get('stdout', None)
    stderr = kwargs.get('stderr', None)

    if isinstance(command, list):
        cmd = ' '.join(command)
    else:
        cmd = command
    try:
        process = subprocess.Popen(cmd, shell=shell, env=env, cwd=path,
                                   stdout=stdout, stderr=stderr)
        atexit.register(subprocess_exit_handler, process)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        raise
    else:
        return process.returncode


def execute_command(command, path, **kwargs):
    """Execute command via thread

    :param command: Command to run. Can be str or list(str)
    :param str path: Path to set as ``cwd``

    Keyword Args:
        shell (bool): Whether to execute subprocess as ``shell``. Defaults to True
        env (dict): Enviroment to set as ``env``
        print_output (bool): Whether to print output. Defaults to True

    :return: Command return code
    :rtype: int
    """

    shell = kwargs.get('shell', True)
    env = kwargs.get('env', None)
    print_output = kwargs.get('print_output', True)

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
        cprint('\n - Command failed\n', 'red')
        return 1
    except Exception as err:
        if pool:
            pool.close()
            pool.terminate()
        cprint('\n - Command failed', 'red')
        print(str(err) + '\n')
        return 1


def execute_forall_command(command, path, forall_env, print_output):
    """Execute forall command with additional environment variables and display continuous output

    :param command: Command to run. Can be str or list(str)
    :param str path: Path to set as ``cwd``
    :param dict forall_env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output
    :return: Command return code
    :rtype: int
    """

    return execute_command(command, path, env=forall_env, print_output=print_output)
