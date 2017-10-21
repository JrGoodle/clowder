"""Process pool"""

import atexit
import multiprocessing as mp
import os
import signal
import subprocess
import sys

import psutil
from termcolor import cprint

from clowder.project import (
    herd_project,
    reset_project,
    run_project,
    sync_project
)
from clowder.util.progress import Progress


def async_callback(val):
    """Increment async progress bar"""
    del val
    PROGRESS.update()


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
        return POOL.apply(execute_subprocess_command,
                          args=(command, path),
                          kwds={'shell': shell, 'env': cmd_env, 'stdout': pipe, 'stderr': pipe})
    except (KeyboardInterrupt, SystemExit):
        return 1
    except Exception as err:
        print(err)
        return 1


def execute_forall_command(command, path, forall_env, print_output):
    """Execute forall command with additional environment variables and display continuous output"""
    return execute_command(command, path, env=forall_env, print_output=print_output)


def herd(projects, branch, tag, depth, rebase):
    """Clone project or update latest from upstream"""
    for project in projects:
        result = POOL.apply_async(herd_project, args=(project, branch, tag, depth, rebase), callback=async_callback)
        RESULTS.append(result)
    pool_handler(len(projects))


def reset(projects):
    """Reset project branches to upstream or checkout tag/sha as detached HEAD"""
    for project in projects:
        result = POOL.apply_async(reset_project, args=(project,), callback=async_callback)
        RESULTS.append(result)
    pool_handler(len(projects))


def run(projects, command, ignore_errors):
    """Run command or script in project directory"""
    for project in projects:
        result = POOL.apply_async(run_project, args=(project, command, ignore_errors), callback=async_callback)
        RESULTS.append(result)
    pool_handler(len(projects))


def sync(projects, rebase):
    """Sync fork project with upstream"""
    for project in projects:
        result = POOL.apply_async(sync_project, args=(project, rebase), callback=async_callback)
        RESULTS.append(result)
    pool_handler(len(projects))


def subprocess_exit_handler(process):
    """terminate subprocess"""
    try:
        os.kill(process.pid, 0)
        process.kill()
    except:
        pass


def execute_subprocess_command(command, path, shell=True, env=None, stdout=None, stderr=None):
    """Run subprocess command"""
    try:
        process = subprocess.Popen(' '.join(command), shell=shell, env=env, cwd=path,
                                   stdout=stdout, stderr=stderr)
        atexit.register(subprocess_exit_handler)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        raise
    else:
        return process.returncode


PARENT_ID = os.getpid()


def worker_init():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """
    def sig_int(signal_num, frame):
        """Signal handler"""
        del signal_num, frame
        # print('signal: %s' % signal_num)
        parent = psutil.Process(PARENT_ID)
        for child in parent.children(recursive=True):
            if child.pid != os.getpid():
                # print("killing child: %s" % child.pid)
                child.terminate()
        # print("killing parent: %s" % parent_id)
        parent.terminate()
        # print("suicide: %s" % os.getpid())
        psutil.Process(os.getpid()).terminate()
        print('\n\n')
    signal.signal(signal.SIGINT, sig_int)


RESULTS = []
POOL = mp.Pool(initializer=worker_init)
PROGRESS = Progress()


def pool_handler(count):
    """Pool handler for finishing parallel jobs"""
    print()
    PROGRESS.start(count)
    try:
        for result in RESULTS:
            result.get()
            if not result.successful():
                PROGRESS.close()
                POOL.close()
                POOL.terminate()
                print()
                cprint(' - Command failed', 'red')
                print()
                sys.exit(1)
    except Exception as err:
        PROGRESS.close()
        POOL.close()
        POOL.terminate()
        print()
        cprint(err, 'red')
        print()
        sys.exit(1)
    else:
        PROGRESS.complete()
        PROGRESS.close()
        POOL.close()
        POOL.join()