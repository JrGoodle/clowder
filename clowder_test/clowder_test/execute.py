# -*- coding: utf-8 -*-
"""Clowder test subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool
from typing import List, Optional, Union

from clowder_test import ROOT_DIR
from clowder_test.clowder_test_error import ClowderTestError


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def execute_test_command(command: str, path: str, parallel: bool = False, write: bool = False,
                         coverage: bool = False, test_env: Optional[dict] = None, debug: bool = False,
                         quiet: bool = False) -> int:
    """Execute test command

    :param str command: Command to run
    :param str path: Path to set as ``cwd``
    :param bool parallel: Whether to run tests in parallel
    :param bool write: Whether to run tests requiring write permission
    :param bool coverage: Whether to run tests with code coverage
    :param Optional[dict] test_env: Custom dict of environment variables
    :param bool debug: Toggle debug output
    :param bool quiet: Suppress all output

    :return: Subprocess return code
    :rtype: int
    """

    test_env = {} if test_env is None else test_env

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

    :raise ClowderTestError:
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
            raise ClowderTestError
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as err:
        raise ClowderTestError(err)


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
    :raise ClowderTestError:
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
        raise ClowderTestError('Command interrupted')
    except Exception as err:
        if pool:
            pool.close()
            pool.terminate()
        raise ClowderTestError(err)
