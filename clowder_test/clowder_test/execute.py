# -*- coding: utf-8 -*-
"""Clowder test subprocess execution utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from clowder_test import ROOT_DIR


def execute_test_command(command: str, path: Path, parallel: bool = False, write: bool = False,
                         coverage: bool = False, test_env: Optional[dict] = None, debug: bool = False) -> None:
    """Execute test command

    :param str command: Command to run
    :param Path path: Path to set as ``cwd``
    :param bool parallel: Whether to run tests in parallel
    :param bool write: Whether to run tests requiring write permission
    :param bool coverage: Whether to run tests with code coverage
    :param Optional[dict] test_env: Custom dict of environment variables
    :param bool debug: Toggle debug output
    """

    test_env = {} if test_env is None else test_env

    test_env['ACCESS_LEVEL'] = 'write' if write else 'read'

    if parallel:
        test_env['PARALLEL'] = '--jobs 4'

    if coverage:
        rc_file = os.path.join(ROOT_DIR, '.coveragerc')
        test_env['COVERAGE_PROCESS_START'] = rc_file
        test_env['COMMAND'] = 'coverage run --rcfile=' + rc_file + ' -m clowder.clowder_app'
    else:
        test_env['COMMAND'] = 'clowder'

    if debug:
        test_env['CLOWDER_DEBUG'] = 'true'

    execute_command(command, path, env=test_env)


def execute_command(command: str, path: Path, env: Optional[dict] = None) -> None:
    """Execute command via subprocess

    :param str command: Command to run
    :param Path path: Path to set as ``cwd``
    :param Optional[dict] env: Enviroment to set as ``env``

    :raise subprocess.CalledProcessError:
    """

    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    subprocess.run(command, shell=True, env=cmd_env, cwd=str(path), check=True)
