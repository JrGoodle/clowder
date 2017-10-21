"""Command execution"""

import atexit
import os
import subprocess

from clowder.util.process_pool import POOL


def execute_command(command, path, shell=True, env=None, print_output=True):
    """Run subprocess command"""
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)
    if print_output:
        pipe = None
    else:
        pipe = subprocess.PIPE
    try:
        result = POOL.apply(_execute_command, args=(command,),
                            kwds={'shell': shell, 'env': cmd_env, 'cwd': path,
                                  'stdout': pipe, 'stderr': pipe, 'print_output': print_output})
        result.get()
    except (KeyboardInterrupt, SystemExit):
        return 1
    except Exception as err:
        return 1
    else:
        return 0


def execute_forall_command(command, path, forall_env, print_output):
    """Execute forall command with additional environment variables and display continuous output"""
    return execute_command(command, path, shell=True, env=forall_env, print_output=print_output)


def _execute_command(command, path, shell=True, env=None, stdout=None, stderr=None, print_output=True):
    """Run subprocess command"""
    try:
        process = subprocess.Popen(' '.join(command), shell=shell, env=env, cwd=path,
                                   stdout=stdout, stderr=stderr)
        # if print_output:
            # atexit.register(subprocess_exit_handler)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as err:
        raise
    else:
        return process.returncode
