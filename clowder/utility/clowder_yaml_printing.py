"""Clowder yaml printing"""

from __future__ import print_function
import os
import sys
from clowder.utility.clowder_utilities import parse_yaml
from clowder.utility.print_utilities import (
    format_path,
    format_symlink_target,
    print_open_file_error,
    remove_prefix
)


def print_yaml(root_directory):
    """Print current clowder yaml"""
    yaml_file = os.path.join(root_directory, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    yaml_files = []
    while True:
        yaml_files.append(yaml_file)
        if 'import' not in parsed_yaml:
            break
        imported_yaml = parsed_yaml['import']
        if imported_yaml == 'default':
            yaml_file = os.path.join(root_directory,
                                     '.clowder',
                                     'clowder.yaml')
        else:
            yaml_file = os.path.join(root_directory,
                                     '.clowder',
                                     'versions',
                                     imported_yaml,
                                     'clowder.yaml')
        parsed_yaml = parse_yaml(yaml_file)
    for yaml_file in yaml_files:
        if os.path.isfile(yaml_file):
            try:
                with open(yaml_file) as raw_file:
                    contents = raw_file.read()
                    print('-' * 80)
                    if os.path.islink(yaml_file):
                        path = format_symlink_target(yaml_file)
                        path = remove_prefix(path, root_directory)
                        path = remove_prefix(path, '/')
                        print()
                        print(format_path('clowder.yaml') + ' -> ' + format_path(path))
                        print()
                    else:
                        path = remove_prefix(yaml_file, root_directory)
                        path = remove_prefix(path, '/')
                        print('\n' + format_path(path) + '\n')
                    print(contents)
            except IOError as err:
                print_open_file_error(yaml_file)
                print(err)
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
