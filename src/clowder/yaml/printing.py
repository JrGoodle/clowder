# -*- coding: utf-8 -*-
"""clowder.yaml printing

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.util.clowder_utils import get_clowder_yaml_import_path
from clowder.yaml.parsing import parse_yaml


def print_yaml():
    """Print current clowder yaml"""

    for yaml_file in _get_yaml_files():
        if os.path.isfile(yaml_file):
            _print_yaml(yaml_file)


def _format_yaml_symlink(yaml_file):
    """Return formatted string for yaml file

    :param str yaml_file: Yaml file path
    """

    path = fmt.symlink_target(yaml_file)
    path = fmt.remove_prefix(path, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.get_path('clowder.yaml') + ' -> ' + fmt.get_path(path) + '\n'


def _format_yaml_file(yaml_file):
    """Return formatted string for yaml file

    :param str yaml_file: Yaml file path
    """

    path = fmt.remove_prefix(yaml_file, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.get_path(path) + '\n'


def _get_yaml_files():
    """Return root yaml file and all yaml files in import chain"""

    yaml_file = os.path.join(ROOT_DIR, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    yaml_files = []
    while True:
        yaml_files.append(yaml_file)
        if 'import' not in parsed_yaml:
            return yaml_files

        yaml_file = get_clowder_yaml_import_path(parsed_yaml['import'])
        parsed_yaml = parse_yaml(yaml_file)


def _print_yaml(yaml_file):
    """Private print current clowder yaml

    :raise ClowderExit:
    """

    try:
        with open(yaml_file) as raw_file:
            contents = raw_file.read()
            print('-' * 80)
            _print_yaml_path(yaml_file)
            print(contents)
    except IOError as err:
        print(fmt.open_file_error(yaml_file))
        print(err)
        raise ClowderExit(1)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def _print_yaml_path(yaml_file):
    """Print clowder yaml path"""

    if os.path.islink(yaml_file):
        print(_format_yaml_symlink(yaml_file))
    else:
        print(_format_yaml_file(yaml_file))
