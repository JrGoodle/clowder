# -*- coding: utf-8 -*-
"""clowder.yaml groups validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.loading import load_yaml_import_projects
from clowder.yaml.util import (
    dict_contains_value,
    validate_optional_ref,
    validate_type,
    validate_type_depth
)
from clowder.yaml.validation.projects import validate_yaml_projects


def load_yaml_import_groups(imported_groups, groups):
    """Load clowder groups from imported yaml

    :param dict imported_groups: Parsed YAML python object for imported groups
    :param dict groups: Parsed YAML python object for groups
    :return:
    """

    group_names = [g['name'] for g in groups]
    for imported_group in imported_groups:
        if imported_group['name'] not in group_names:
            groups.append(imported_group)
            continue
        combined_groups = []
        for group in groups:
            if group['name'] == imported_group['name']:
                if 'recursive' in imported_group:
                    group['recursive'] = imported_group['recursive']
                if 'ref' in imported_group:
                    group['ref'] = imported_group['ref']
                if 'remote' in imported_group:
                    group['remote'] = imported_group['remote']
                if 'source' in imported_group:
                    group['source'] = imported_group['source']
                if 'depth' in imported_group:
                    group['depth'] = imported_group['depth']
                if 'timestamp_author' in imported_group:
                    group['timestamp_author'] = imported_group['timestamp_author']
                if 'projects' in imported_group:
                    load_yaml_import_projects(imported_group['projects'], group['projects'])
            combined_groups.append(group)
        groups = combined_groups


def validate_yaml_import_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file with import

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(groups, 'groups', list, 'list', yaml_file)

    if not groups:
        error = fmt.missing_entries_error('groups', yaml_file)
        raise ClowderError(error)

    for group in groups:
        validate_yaml_import_group(group, yaml_file)


def validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(groups, 'groups', list, 'list', yaml_file)

    if not groups:
        error = fmt.missing_entries_error('groups', yaml_file)
        raise ClowderError(error)

    for group in groups:
        validate_yaml_group(group, yaml_file)


def validate_yaml_import_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file with import

    :param dict group: Parsed YAML python object for group
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(group, 'group', dict, 'dict', yaml_file)

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    dict_contains_value(group, 'group', 'name', yaml_file)
    validate_type(group['name'], 'name', str, 'str', yaml_file)
    del group['name']

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    if 'projects' in group:
        validate_yaml_projects(group['projects'], yaml_file, is_import=True)
        del group['projects']

    if 'recursive' in group:
        validate_type(group['recursive'], 'recursive', bool, 'bool', yaml_file)
        del group['recursive']

    validate_optional_ref(group, yaml_file)

    if 'remote' in group:
        validate_type(group['remote'], 'remote', str, 'str', yaml_file)
        del group['remote']

    if 'source' in group:
        validate_type(group['source'], 'source', str, 'str', yaml_file)
        del group['source']

    if 'depth' in group:
        validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if 'timestamp_author' in group:
        validate_type(group['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del group['timestamp_author']

    if group:
        error = fmt.unknown_entry_error('group', group, yaml_file)
        raise ClowderError(error)


def validate_yaml_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file

    :param dict group: Parsed YAML python object for group
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(group, 'group', dict, 'dict', yaml_file)

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    dict_contains_value(group, 'group', 'name', yaml_file)
    validate_type(group['name'], 'name', str, 'str', yaml_file)
    del group['name']

    dict_contains_value(group, 'group', 'projects', yaml_file)
    validate_yaml_projects(group['projects'], yaml_file, is_import=False)
    del group['projects']

    if 'recursive' in group:
        validate_type(group['recursive'], 'recursive', bool, 'bool', yaml_file)
        del group['recursive']

    if 'timestamp_author' in group:
        validate_type(group['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del group['timestamp_author']

    validate_optional_ref(group, yaml_file)

    if 'remote' in group:
        validate_type(group['remote'], 'remote', str, 'str', yaml_file)
        del group['remote']

    if 'source' in group:
        validate_type(group['source'], 'source', str, 'str', yaml_file)
        del group['source']

    if 'depth' in group:
        validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if group:
        error = fmt.unknown_entry_error('group', group, yaml_file)
        raise ClowderError(error)
