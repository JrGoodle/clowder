# -*- coding: utf-8 -*-
"""Clowder test subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool

from termcolor import cprint

from clowder_test import ROOT_DIR
from clowder_test.clowder_test_error import ClowderTestError


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def execute_test_command(command, path, **kwargs):
    """Execute test command

    .. py:function:: execute_test_command(command, path, parallel=False, write=False, coverage=False, test_env=None)

    :param command: Command to run
    :type command: str
    :param str path: Path to set as ``cwd``

    Keyword Args:
        parallel (bool): Whether to run tests in parallel
        write (bool): Whether to run tests requiring write permission
        coverage (bool): Whether to run tests with code coverage
        test_env (dict): Custom dict of environment variables

    :return: Subprocess return code
    :rtype: int
    """

    parallel = kwargs.get('parallel', False)
    write = kwargs.get('write', False)
    coverage = kwargs.get('coverage', False)
    test_env = kwargs.get('test_env', {})

    test_env['ACCESS_LEVEL'] = 'write' if write else 'read'

    if parallel:
        test_env['PARALLEL'] = '--parallel'

    if coverage:
        rc_file = os.path.join(ROOT_DIR, '.coveragerc')
        test_env['COMMAND'] = 'coverage run --rcfile=' + rc_file + ' -m clowder.clowder_app'
    else:
        test_env['COMMAND'] = 'clowder'

    execute_command(command, path, env=test_env)


def subprocess_exit_handler(process):
    """terminate subprocess"""

    try:
        process.terminate()
    except Exception as err:
        del err


def execute_subprocess_command(command, path, **kwargs):
    """Execute subprocess command

    .. py:function:: execute_subprocess_command(command, path, shell=True, env=None, stdout=None, stderr=None)

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``

    Keyword Args:
        shell (bool): Whether to execute subprocess as ``shell``
        env (dict): Enviroment to set as ``env``
        stdout (int): Value to set as ``stdout``
        stderr (int): Value to set as ``stderr``

    :return: Subprocess return code
    :rtype: int
    :raise ClowderTestError:
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
        if process.returncode != 0:
            raise ClowderTestError
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as err:
        raise ClowderTestError(err)


def execute_command(command, path, **kwargs):
    """Execute command via thread

    .. py:function:: execute_command(command, path, shell=True, env=None, print_output=True)

    :param command: Command to run
    :type command: str or list[str]
    :param str path: Path to set as ``cwd``

    Keyword Args:
        shell (bool): Whether to execute subprocess as ``shell``
        env (dict): Enviroment to set as ``env``
        print_output (bool): Whether to print output

    :return: Command return code
    :rtype: int
    :raise ClowderTestError:
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
        raise ClowderTestError('Command interrupted')
    except Exception as err:
        if pool:
            pool.close()
            pool.terminate()
        raise ClowderTestError(err)
