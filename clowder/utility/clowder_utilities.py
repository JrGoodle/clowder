"""Clowder utilities"""

from __future__ import print_function
import errno
import os
import shutil
import socket
import subprocess
import sys
import yaml
from termcolor import colored, cprint
from clowder.utility.print_utilities import (
    format_empty_yaml_error,
    format_path,
    print_file_exists_error,
    print_invalid_yaml_error,
    print_missing_yaml_error,
    print_open_file_error,
    print_save_file_error
)


def execute_command(command, path, shell=True, env=None, print_output=True):
    """Run subprocess command"""
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)
    try:
        if print_output:
            process = subprocess.Popen(' '.join(command), shell=shell, env=cmd_env, cwd=path)
        else:
            process = subprocess.Popen(' '.join(command), shell=shell, env=cmd_env, cwd=path,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # atexit.register(subprocess_exit_handler, process)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        process.kill()
    return process.returncode


def execute_forall_command(command, path, forall_env, print_output):
    """Execute forall command with additional environment variables and display continuous output"""
    return execute_command(command, path, shell=True, env=forall_env, print_output=print_output)


def existing_git_repository(path):
    """Check if a git repository exists"""
    return os.path.isdir(os.path.join(path, '.git'))


def existing_git_submodule(path):
    """Check if a git submodule exists"""
    return os.path.isfile(os.path.join(path, '.git'))


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


def get_yaml_string(yaml_output):
    """Return yaml string from python data structures"""
    try:
        return yaml.safe_dump(yaml_output, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        cprint('Failed to dump yaml', 'red')
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
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


def parse_yaml(yaml_file):
    """Parse yaml file"""
    if os.path.isfile(yaml_file):
        try:
            with open(yaml_file) as raw_file:
                parsed_yaml = yaml.safe_load(raw_file)
                if parsed_yaml is None:
                    print_invalid_yaml_error()
                    print(format_empty_yaml_error(yaml_file) + '\n')
                    sys.exit(1)
                return parsed_yaml
        except yaml.YAMLError:
            print_open_file_error(yaml_file)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        print()
        print_missing_yaml_error()
        print()
        sys.exit(1)


def ref_type(ref):
    """Return branch, tag, sha, or unknown ref type"""
    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return 'branch'
    elif ref.startswith(git_tag):
        return 'tag'
    elif len(ref) == 40:
        return 'sha'
    return 'unknown'


def remove_directory(path):
    """Remove directory at path"""
    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + format_path(path))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk"""
    if not os.path.isfile(yaml_file):
        try:
            with open(yaml_file, 'w') as raw_file:
                print(" - Save yaml to file")
                yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
        except yaml.YAMLError:
            print_save_file_error(yaml_file)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        print_file_exists_error(yaml_file)
        print()
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
