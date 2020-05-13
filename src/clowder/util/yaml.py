# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
import os
from typing import List, Optional

# noinspection PyPackageRequirements
import jsonschema
# noinspection PyPackageRequirements
import yaml as pyyaml

import clowder.util.formatting as fmt
from clowder import ROOT_DIR, CLOWDER_SCHEMA
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError, ClowderYAMLYErrorType


def load_yaml() -> dict:
    """Load clowder from yaml file

    :return: YAML python object
    :rtype: dict
    :raise ClowderYAMLError:
    """

    yaml_file = os.path.join(ROOT_DIR, 'clowder.yaml')
    validate_yaml(yaml_file)
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
        raise ClowderYAMLError(fmt.error_missing_yaml(), ClowderYAMLYErrorType.MISSING_YAML)

    try:
        with open(yaml_file) as raw_file:
            parsed_yaml = pyyaml.safe_load(raw_file)
            if parsed_yaml is None:
                raise ClowderYAMLError(fmt.error_empty_yaml(yaml_file), ClowderYAMLYErrorType.EMPTY_YAML)
            return parsed_yaml
    except pyyaml.YAMLError:
        raise ClowderYAMLError(fmt.error_open_file(yaml_file), ClowderYAMLYErrorType.OPEN_FILE)
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
        print(fmt.error_file_exists(yaml_file) + '\n')
        raise ClowderExit(1)

    try:
        with open(yaml_file, 'w') as raw_file:
            print(" - Save yaml to file")
            pyyaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except pyyaml.YAMLError:
        print(fmt.error_save_file(yaml_file))
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

    json_schema = _load_json_schema()
    parsed_yaml = parse_yaml(yaml_file)
    parsed_yaml_copy = copy.deepcopy(parsed_yaml)
    try:
        jsonschema.validate(parsed_yaml, json_schema)
    except jsonschema.exceptions.ValidationError as err:
        error_message = f"{fmt.error_invalid_yaml()}\n{fmt.ERROR} {err.message}"
        raise ClowderYAMLError(error_message, ClowderYAMLYErrorType.UNKNOWN)

    _validate_yaml_contents(parsed_yaml_copy, yaml_file)


def _check_for_duplicates(list_of_elements: List[str]) -> Optional[str]:
    """Check if given list contains any duplicates

    :param List[str] list_of_elements: List of strings to check for duplicates
    :return: First duplicate encountered, or None if no duplicates found
    :rtype: Optional[str]
    """

    set_of_elements = set()
    for elem in list_of_elements:
        if elem in set_of_elements:
            return elem
        else:
            set_of_elements.add(elem)
    return None


def _format_yaml_symlink(yaml_file: str) -> str:
    """Return formatted string for yaml symlink

    :param str yaml_file: Yaml file path
    :return: Formatted string for yaml symlink
    :rtype: str
    """

    path = fmt.symlink_target(yaml_file)
    path = fmt.remove_prefix(path, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.path_string('clowder.yaml') + ' -> ' + fmt.path_string(path) + '\n'


def _format_yaml_file(yaml_file: str) -> str:
    """Return formatted string for yaml file

    :param str yaml_file: Yaml file path
    :return: Formatted string for yaml file
    :rtype: str
    """

    path = fmt.remove_prefix(yaml_file, ROOT_DIR)
    path = fmt.remove_prefix(path, '/')
    return '\n' + fmt.path_string(path) + '\n'


def _load_json_schema() -> dict:
    """Return json schema file

    :return: Loaded json dict
    :rtype: dict
    """

    return pyyaml.safe_load(CLOWDER_SCHEMA)


def _print_yaml(yaml_file: str) -> None:
    """Private print current clowder yaml

    :param str yaml_file: Path to yaml file
    :raise ClowderExit:
    """

    try:
        with open(yaml_file) as raw_file:
            contents = raw_file.read()
            print('-' * 80)
            _print_yaml_path(yaml_file)
            print(contents)
    except IOError as err:
        print(fmt.error_open_file(yaml_file))
        print(err)
        raise ClowderExit(1)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def _print_yaml_path(yaml_file: str) -> None:
    """Print clowder yaml path

    :param str yaml_file: Path to yaml file
    """

    if os.path.islink(yaml_file):
        print(_format_yaml_symlink(yaml_file))
    else:
        print(_format_yaml_file(yaml_file))


def _validate_yaml_contents(yaml: dict, yaml_file: str) -> None:
    """Validate contents in clowder loaded from yaml file

    :param dict yaml: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    """

    err_prefix = f"{fmt.error_invalid_yaml()}\n{fmt.ERROR} "

    sources = []
    for source in yaml['sources']:
        sources.append(source['name'])

    defaults = yaml['defaults']
    # Validate default source is defined in sources
    if defaults['source'] not in sources:
        err = f"{err_prefix}{fmt.error_source_default_not_found(defaults['source'], yaml_file)}"
        raise ClowderYAMLError(err, ClowderYAMLYErrorType.SOURCE_NOT_FOUND)

    projects = []
    projects_with_forks = []
    for p in yaml['projects']:
        project = {'name': p['name'],
                   'path': p.get('path', p['name'])}
        if 'remote' in p:
            project['remote'] = p['remote']
        if 'source' in p:
            # Validate custom project source is defined in sources
            if p['source'] not in sources:
                err = f"{err_prefix}{fmt.error_source_not_found(p['source'], yaml_file, project['name'])}"
                raise ClowderYAMLError(err, ClowderYAMLYErrorType.SOURCE_NOT_FOUND)
        projects.append(project)
        if 'fork' in p:
            f = p['fork']
            fork = {'name': f['name']}
            if 'remote' in f:
                fork['remote'] = f['remote']
            if 'source' in f:
                # Validate custom fork source is defined in sources
                if f['source'] not in sources:
                    err = f"{err_prefix}{fmt.error_source_not_found(f['source'], yaml_file, project['name'])}"
                    raise ClowderYAMLError(err, ClowderYAMLYErrorType.SOURCE_NOT_FOUND)
            project['fork'] = fork
            projects_with_forks.append(project)

    # Validate projects and forks have different remote names
    for project in projects_with_forks:
        fork = project['fork']
        default_remote = defaults['remote']
        if 'remote' in project and 'remote' in fork:
            if project['remote'] == fork['remote']:
                err = f"{err_prefix}{fmt.error_remote_dup(fork['name'], project['name'], project['remote'], yaml_file)}"
                raise ClowderYAMLError(err, ClowderYAMLYErrorType.DUPLICATE_REMOTE_NAME)
        elif 'remote' in project:
            if project['remote'] == default_remote:
                err = f"{err_prefix}{fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)}"
                raise ClowderYAMLError(err, ClowderYAMLYErrorType.DUPLICATE_REMOTE_NAME)
        elif 'remote' in fork:
            if fork['remote'] == default_remote:
                err = f"{err_prefix}{fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)}"
                raise ClowderYAMLError(err, ClowderYAMLYErrorType.DUPLICATE_REMOTE_NAME)
        else:
            err = f"{err_prefix}{fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)}"
            raise ClowderYAMLError(err, ClowderYAMLYErrorType.DUPLICATE_REMOTE_NAME)

    # Validate projects don't share share directories
    paths = [p['path'] for p in projects]
    duplicate = _check_for_duplicates(paths)
    if duplicate is not None:
        err = f"{err_prefix}{fmt.error_duplicate_project_path(duplicate, yaml_file)}"
        raise ClowderYAMLError(err, ClowderYAMLYErrorType.DUPLICATE_PATH)
