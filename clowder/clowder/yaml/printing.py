# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import clowder.util.formatting as fmt
from clowder.yaml.parsing import parse_yaml


def print_yaml(root_directory):
    """Print current clowder yaml

    :param str root_directory: Path to root directory containing clowder.yaml symlink
    :return:
    """

    yaml_file = os.path.join(root_directory, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    yaml_files = []
    while True:
        yaml_files.append(yaml_file)
        if 'import' not in parsed_yaml:
            break

        imported_yaml = parsed_yaml['import']
        if imported_yaml == 'default':
            yaml_file = os.path.join(root_directory, '.clowder', 'clowder.yaml')
        else:
            yaml_file = os.path.join(root_directory, '.clowder', 'versions', imported_yaml, 'clowder.yaml')
        parsed_yaml = parse_yaml(yaml_file)

    for yaml_file in yaml_files:
        if os.path.isfile(yaml_file):
            try:
                with open(yaml_file) as raw_file:
                    contents = raw_file.read()
                    print('-' * 80)
                    if os.path.islink(yaml_file):
                        path = fmt.symlink_target(yaml_file)
                        path = fmt.remove_prefix(path, root_directory)
                        path = fmt.remove_prefix(path, '/')
                        print('\n' + fmt.get_path('clowder.yaml') + ' -> ' + fmt.get_path(path) + '\n')
                    else:
                        path = fmt.remove_prefix(yaml_file, root_directory)
                        path = fmt.remove_prefix(path, '/')
                        print('\n' + fmt.get_path(path) + '\n')
                    print(contents)
            except IOError as err:
                print(fmt.open_file_error(yaml_file))
                print(err)
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
