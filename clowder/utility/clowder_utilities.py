"""Clowder utilities"""
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

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for too many arguments
# pylint: disable=R0913
# Disable errors shown by pylint for invalid function name
# pylint: disable=C0103

def execute_command(cmd, path):
    """Execute command and display continuous output"""
    return subprocess.call(" ".join(cmd),
                           shell=True,
                           cwd=path)

def execute_forall_command(cmd, path, clowder_path, name, remote, fork_remote, ref):
    """Execute forall command with additional environment variables and display continuous output"""
    forall_env = os.environ.copy()
    forall_env["CLOWDER_PATH"] = clowder_path
    forall_env["PROJECT_PATH"] = path
    forall_env["PROJECT_NAME"] = name
    forall_env["PROJECT_REMOTE"] = remote
    forall_env["PROJECT_REF"] = ref
    if fork_remote is not None:
        forall_env["FORK_REMOTE"] = fork_remote
    return subprocess.call(" ".join(cmd),
                           shell=True,
                           cwd=path,
                           env=forall_env)

def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)

def get_yaml_string(yaml_output):
    """Return yaml string from python data structures"""
    try:
        return yaml.dump(yaml_output, default_flow_style=False, indent=4)
    except:
        cprint('Failed to dump yaml', 'red')
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
    except:
        return True

def parse_yaml(yaml_file):
    """Parse yaml file"""
    if os.path.isfile(yaml_file):
        try:
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)
                if parsed_yaml is None:
                    print_invalid_yaml_error()
                    print(format_empty_yaml_error(yaml_file) + '\n')
                    sys.exit(1)
                return parsed_yaml
        except:
            print_open_file_error(yaml_file)
            sys.exit(1)
    else:
        print()
        print_missing_yaml_error()
        print()
        sys.exit(1)

def remove_directory_exit(path):
    """Remove directory at path"""
    try:
        shutil.rmtree(path)
    except:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + format_path(path))
    finally:
        print()
        sys.exit(1)

def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk"""
    if not os.path.isfile(yaml_file):
        try:
            with open(yaml_file, 'w') as file:
                print(" - Save yaml to file")
                yaml.dump(yaml_output, file, default_flow_style=False, indent=4)
        except:
            print_save_file_error(yaml_file)
            sys.exit(1)
    else:
        print_file_exists_error(yaml_file)
        print()
        sys.exit(1)
