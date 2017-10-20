"""Clowder utilities"""

from __future__ import print_function
import errno
import os
import shutil
import socket
import subprocess
import sys

from termcolor import colored

import clowder.utility.formatting as fmt


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


def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)
    except (KeyboardInterrupt, SystemExit):
        os.remove(file2)
        os.symlink(file1, file2)
        sys.exit(1)


def is_offline(host='8.8.8.8', port=53, timeout=3):
    """
    Returns True if offline, False otherwise
    Source: https://stackoverflow.com/a/33117579
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return False
    except socket.error:
        return True
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def remove_directory(path):
    """Remove directory at path"""
    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + fmt.path(path))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def truncate_ref(ref):
    """Return bare branch, tag, or sha"""
    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        length = len(git_branch)
    elif ref.startswith(git_tag):
        length = len(git_tag)
    else:
        length = 0
    return ref[length:]
