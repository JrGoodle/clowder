"""Clowder utilities"""
import errno
import os
import subprocess
import sys
import yaml
from clowder.utility.print_utilities import (
    format_empty_yaml_error,
    print_file_exists_error,
    print_invalid_yaml_error,
    print_missing_yaml_error,
    print_open_file_error,
    print_save_file_error
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def execute_command(cmd, path):
    """Execute command and display continuous output"""
    return subprocess.call(" ".join(cmd),
                           shell=True,
                           cwd=path)

def execute_command_popen(cmd, path):
    """Execute command and display continuous output"""
    for output in execute_popen(cmd, path):
        print(output, end='')

def execute_popen(cmd, path):
    """Execute command"""
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(cmd, cwd=path,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    # print("the commandline is {}".format(process.args))
    for stdout_line in iter(process.stdout.readline, ''):
        yield stdout_line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)

def parse_yaml(yaml_file):
    """Parse yaml file"""
    if os.path.isfile(yaml_file):
        try:
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)
                if parsed_yaml is None:
                    print_invalid_yaml_error()
                    print(format_empty_yaml_error(yaml_file))
                    sys.exit(1)
                else:
                    return parsed_yaml
        except:
            print_open_file_error(yaml_file)
            sys.exit(1)
    else:
        print()
        print_missing_yaml_error()
        print()
        sys.exit(1)

def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk"""
    if not os.path.isfile(yaml_file):
        try:
            with open(yaml_file, 'w') as file:
                print(" - Save yaml to file")
                yaml.dump(yaml_output, file, default_flow_style=False)
        except:
            print_save_file_error(yaml_file)
            sys.exit(1)
    else:
        print_file_exists_error(yaml_file)
        print()
        sys.exit(1)
