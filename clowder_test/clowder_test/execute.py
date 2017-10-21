"""Command execution"""

import atexit
import os
import signal
import subprocess

import psutil


def execute_command(command, path, shell=True, env=None):
    """Run subprocess command"""
    cmd_env = os.environ.copy()
    process = None
    if env:
        cmd_env.update(env)
    try:
        process = subprocess.Popen(' '.join(command), shell=shell, env=cmd_env, cwd=path)
        atexit.register(subprocess_exit_handler)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        return 1
    except Exception as err:
        print(err)
        return 1
    else:
        return process.returncode


PARENT_ID = os.getpid()


def subprocess_exit_handler():
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
