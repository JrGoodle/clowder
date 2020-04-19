# -*- coding: utf-8 -*-
"""Clowder test subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool
from typing import List, Union

from clowder_test import ROOT_DIR
from clowder_test.clowder_test_error import ClowderTestError


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def execute_test_command(command: str, path: str, **kwargs) -> int:
    """Execute test command

    .. py:function:: execute_test_command(command, path, parallel=False, write=False, coverage=False, test_env=None, debug=False, quiet=False, ssh=False)

    :param str command: Command to run
    :param str path: Path to set as ``cwd``

    Keyword Args:
        parallel (bool): Whether to run tests in parallel
        write (bool): Whether to run tests requiring write permission
        coverage (bool): Whether to run tests with code coverage
        test_env (dict): Custom dict of environment variables
        debug (bool): Toggle debug output
        quiet (bool): Suppress all output
        ssh (bool): Whether to run test scripts requiring ssh credentials

    :return: Subprocess return code
    :rtype: int
    """

    parallel = kwargs.get('parallel', False)
    write = kwargs.get('write', False)
    coverage = kwargs.get('coverage', False)
    test_env = kwargs.get('test_env', {})
    debug = kwargs.get('debug', False)
    quiet = kwargs.get('quiet', False)

    test_env['ACCESS_LEVEL'] = 'write' if write else 'read'

    if parallel:
        test_env['PARALLEL'] = '--parallel'

    if coverage:
        rc_file = os.path.join(ROOT_DIR, '.coveragerc')
        test_env['COVERAGE_PROCESS_START'] = rc_file
        test_env['COMMAND'] = 'coverage run --rcfile=' + rc_file + ' -m clowder.clowder_app'
    else:
        test_env['COMMAND'] = 'clowder'

    if debug:
        test_env['COMMAND'] = test_env['COMMAND'] + ' --debug'

    if quiet:
        test_env['COMMAND'] = test_env['COMMAND'] + ' --quiet'
        execute_command(command, path, print_output=False, env=test_env)
    else:
        return execute_command(command, path, env=test_env)


def subprocess_exit_handler(process: subprocess.Popen):
    """terminate subprocess

    :param subprocess.Popen process: Process
    """

    try:
        process.terminate()
    except Exception as err:
        del err


def execute_subprocess_command(command: Union[str, List[str]], path: str, **kwargs) -> None:
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


def execute_command(command: Union[str, List[str]], path: str, **kwargs) -> int:
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
