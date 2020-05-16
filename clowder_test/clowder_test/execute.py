# -*- coding: utf-8 -*-
"""Clowder test subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import subprocess
from functools import wraps
from typing import Optional

from clowder_test import ROOT_DIR


def create_cats_cache(func):
    """Create cats cache"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        path = os.path.join(ROOT_DIR, 'test', 'scripts')
        execute_test_command('./create_cache.sh cats', path)
        return func(*args, **kwargs)

    return wrapper


def create_misc_cache(func):
    """Create misc cache"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        path = os.path.join(ROOT_DIR, 'test', 'scripts')
        execute_test_command('./create_cache.sh misc', path)
        return func(*args, **kwargs)

    return wrapper


def create_swift_cache(func):
    """Create swift cache"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        path = os.path.join(ROOT_DIR, 'test', 'scripts')
        execute_test_command('./create_cache.sh swift', path)
        return func(*args, **kwargs)

    return wrapper


def execute_test_command(command: str, path: str, parallel: bool = False, write: bool = False,
                         coverage: bool = False, test_env: Optional[dict] = None, debug: bool = True,
                         quiet: bool = False) -> None:
    """Execute test command

    :param str command: Command to run
    :param str path: Path to set as ``cwd``
    :param bool parallel: Whether to run tests in parallel
    :param bool write: Whether to run tests requiring write permission
    :param bool coverage: Whether to run tests with code coverage
    :param Optional[dict] test_env: Custom dict of environment variables
    :param bool debug: Toggle debug output
    :param bool quiet: Suppress all output
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

    print_output = not quiet

    execute_command(command, path, print_output=print_output, env=test_env)


def execute_command(command: str, path: str, env: Optional[dict] = None, print_output: bool = True) -> None:
    """Execute command via subprocess

    :param str command: Command to run
    :param str path: Path to set as ``cwd``
    :param Optional[dict] env: Enviroment to set as ``env``
    :param bool print_output: Whether to print output

    :raise subprocess.CalledProcessError:
    """

    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    pipe = None if print_output else subprocess.PIPE

    subprocess.run(command, shell=True, env=cmd_env, cwd=path, stdout=pipe, stderr=pipe, check=True)
