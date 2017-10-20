"""Command execution"""

import atexit
import os
import signal
import subprocess

import psutil


def execute_command(command, path, shell=True, env=None, print_output=True):
    """Run subprocess command"""
    cmd_env = os.environ.copy()
    process = None
    if env:
        cmd_env.update(env)
    if print_output:
        pipe = None
    else:
        pipe = subprocess.PIPE
    try:
        process = subprocess.Popen(' '.join(command), shell=shell, env=cmd_env, cwd=path, stdout=pipe, stderr=pipe)
        atexit.register(subprocess_exit_handler)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        if process:
            process.terminate()
        return 1
    else:
        return process.returncode


def execute_forall_command(command, path, forall_env, print_output):
    """Execute forall command with additional environment variables and display continuous output"""
    return execute_command(command, path, shell=True, env=forall_env, print_output=print_output)


PARENT_ID = os.getpid()


def subprocess_exit_handler():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """

    def sig_int(signal_num, frame):
        """Signal handler"""
        # print('signal: %s' % signal_num)
        parent = psutil.Process(PARENT_ID)
        for child in parent.children():
            if child.pid != os.getpid():
                # print("killing child: %s" % child.pid)
                child.terminate()
        # print("killing parent: %s" % parent_id)
        parent.terminate()
        # print("suicide: %s" % os.getpid())
        psutil.Process(os.getpid()).terminate()
        print('\n\n')
    signal.signal(signal.SIGINT, sig_int)