# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

# noinspection PyPackageRequirements
import yaml

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError, ClowderYAMLYErrorType
from clowder.util.validation import (
    validate_required_dict,
    validate_type,
    validate_yaml_defaults,
    validate_yaml_groups,
    validate_yaml_sources
)


def load_yaml() -> dict:
    """Load clowder from yaml file

    :raise ClowderYAMLError:
    """

    yaml_file = os.path.join(ROOT_DIR, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    if 'depth' not in parsed_yaml['defaults']:
        parsed_yaml['defaults']['depth'] = 0

    return parsed_yaml


def parse_yaml(yaml_file: str) -> dict:
    """Parse yaml file

    :param str yaml_file: Path to yaml file
    :return: YAML python object
    :rtype: dict
    Raises:
        ClowderExit
        ClowderYAMLError
    """

    if not os.path.isfile(yaml_file):
        raise ClowderYAMLError(fmt.missing_yaml_error(), ClowderYAMLYErrorType.MISSING_YAML)

    try:
        with open(yaml_file) as raw_file:
            parsed_yaml = yaml.safe_load(raw_file)
            if parsed_yaml is None:
                raise ClowderYAMLError(fmt.empty_yaml_error(yaml_file), ClowderYAMLYErrorType.EMPTY_YAML)
            return parsed_yaml
    except yaml.YAMLError:
        raise ClowderYAMLError(fmt.open_file_error(yaml_file), ClowderYAMLYErrorType.OPEN_FILE)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def print_yaml() -> None:
    """Print current clowder yaml"""

    yaml_file = os.path.join(ROOT_DIR, 'clowder.yaml')
    if os.path.isfile(yaml_file):
        _print_yaml(yaml_file)


def save_yaml(yaml_output: dict, yaml_file: str) -> None:
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param str yaml_file: Path to save yaml file
    :raise ClowderExit:
    """

    if os.path.isfile(yaml_file):
        print(fmt.file_exists_error(yaml_file) + '\n')
        raise ClowderExit(1)

    try:
        with open(yaml_file, 'w') as raw_file:
            print(" - Save yaml to file")
            yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        print(fmt.save_file_error(yaml_file))
        raise ClowderExit(1)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def validate_yaml(yaml_file: str) -> None:
    """Validate clowder.yaml

    :param str yaml_file: Yaml file path to validate
    Raises:
        ClowderExit
        ClowderYAMLError
    """

    parsed_yaml = parse_yaml(yaml_file)
    validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    if not parsed_yaml:
        raise ClowderYAMLError(fmt.empty_yaml_error(yaml_file), ClowderYAMLYErrorType.EMPTY_YAML)

    validate_required_dict(parsed_yaml, 'defaults', validate_yaml_defaults, yaml_file)
    validate_required_dict(parsed_yaml, 'sources', validate_yaml_sources, yaml_file)
    validate_required_dict(parsed_yaml, 'groups', validate_yaml_groups, yaml_file)

    if parsed_yaml:
        raise ClowderYAMLError(fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file),
                               ClowderYAMLYErrorType.UNKNOWN_ENTRY)


def _format_yaml_symlink(yaml_file: str) -> str:
    """Return formatted string for yaml file

    :param str yaml_file: Yaml file path
    """

    path = fmt.symlink_target(yaml_file)
    path = fmt.remove_prefix(path, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.get_path('clowder.yaml') + ' -> ' + fmt.get_path(path) + '\n'


def _format_yaml_file(yaml_file: str) -> str:
    """Return formatted string for yaml file

    :param str yaml_file: Yaml file path
    """

    path = fmt.remove_prefix(yaml_file, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.get_path(path) + '\n'


def _print_yaml(yaml_file) -> None:
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


def _print_yaml_path(yaml_file) -> None:
    """Print clowder yaml path"""

    if os.path.islink(yaml_file):
        print(_format_yaml_symlink(yaml_file))
    else:
        print(_format_yaml_file(yaml_file))
