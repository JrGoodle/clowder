"""Subprocess execution"""

from __future__ import print_function

import atexit
import os
import subprocess
from multiprocessing.pool import ThreadPool

from termcolor import cprint


# Disable errors shown by pylint for catching too general exception
# pylint: disable=W0703


def subprocess_exit_handler(process):
    """terminate subprocess"""

    try:
        process.terminate()
    except Exception as err:
        del err


def execute_subprocess_command(command, path, shell=True, env=None, stdout=None, stderr=None):
    """Execute subprocess command"""

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
    except Exception as err:
        print(err)
        raise
    else:
        return process.returncode


def execute_command(command, path, shell=True, env=None, print_output=True):
    """Execute command via thread"""

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
        print()
        cprint(' - Command failed', 'red')
        print()
        return 1
    except Exception as err:
        if pool:
            pool.close()
            pool.terminate()
        print()
        cprint(' - Command failed', 'red')
        print(err)
        print()
        return 1
