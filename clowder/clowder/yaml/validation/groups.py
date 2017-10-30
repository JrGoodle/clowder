# -*- coding: utf-8 -*-
"""clowder.yaml groups validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    dict_contains_value,
    validate_optional_ref,
    validate_optional_bool,
    validate_optional_string,
    validate_required_string,
    validate_type,
    validate_type_depth
)
from clowder.yaml.validation.projects import validate_yaml_projects


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

    validate_required_string(group, 'group', 'name', yaml_file)

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    if 'projects' in group:
        validate_yaml_projects(group['projects'], yaml_file, is_import=True)
        del group['projects']

    validate_optional_bool(group, 'recursive', yaml_file)
    validate_optional_string(group, 'remote', yaml_file)
    validate_optional_string(group, 'source', yaml_file)
    validate_optional_string(group, 'timestamp_author', yaml_file)

    validate_optional_ref(group, yaml_file)

    if 'depth' in group:
        validate_type_depth(group['depth'], yaml_file)
        del group['depth']

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

    validate_required_string(group, 'group', 'name', yaml_file)

    dict_contains_value(group, 'group', 'projects', yaml_file)
    validate_yaml_projects(group['projects'], yaml_file, is_import=False)
    del group['projects']

    validate_optional_bool(group, 'recursive', yaml_file)

    string_args = ['remote', 'source', 'timestamp_author']
    for arg in string_args:
        validate_optional_string(group, arg, yaml_file)

    validate_optional_ref(group, yaml_file)

    if 'depth' in group:
        validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if group:
        error = fmt.unknown_entry_error('group', group, yaml_file)
        raise ClowderError(error)
