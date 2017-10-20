"""Network connectivity"""


import os
import subprocess


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
