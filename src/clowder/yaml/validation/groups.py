# -*- coding: utf-8 -*-
"""clowder.yaml groups validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.yaml.validation.projects import (
    validate_yaml_projects_import,
    validate_yaml_projects
)
from clowder.yaml.validation.util import (
    validate_dict_contains_value,
    validate_depth,
    validate_empty,
    validate_not_empty,
    validate_optional_ref,
    validate_optional_bool,
    validate_optional_string,
    validate_required_string,
    validate_type
)


def validate_yaml_groups_import(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file with import

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    """

    validate_type(groups, 'groups', list, 'list', yaml_file)
    validate_not_empty(groups, 'groups', yaml_file)

    for group in groups:
        validate_type(group, 'group', dict, 'dict', yaml_file)
        validate_not_empty(group, 'group', yaml_file)

        validate_required_string(group, 'group', 'name', yaml_file)
        validate_not_empty(group, 'group', yaml_file)

        if 'projects' in group:
            validate_yaml_projects_import(group['projects'], yaml_file)
            del group['projects']

        validate_optional_bool(group, 'recursive', yaml_file)
        validate_depth(group, yaml_file)
        validate_optional_ref(group, yaml_file)

        args = ['remote', 'source', 'timestamp_author']
        for arg in args:
            validate_optional_string(group, arg, yaml_file)

        validate_empty(group, 'group', yaml_file)


def validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    """

    validate_type(groups, 'groups', list, 'list', yaml_file)
    validate_not_empty(groups, 'groups', yaml_file)

    for group in groups:
        validate_type(group, 'group', dict, 'dict', yaml_file)
        validate_not_empty(group, 'group', yaml_file)

        validate_required_string(group, 'group', 'name', yaml_file)

        validate_dict_contains_value(group, 'group', 'projects', yaml_file)
        validate_yaml_projects(group['projects'], yaml_file)
        del group['projects']

        validate_depth(group, yaml_file)
        validate_optional_bool(group, 'recursive', yaml_file)
        validate_optional_ref(group, yaml_file)

        string_args = ['remote', 'source', 'timestamp_author']
        for arg in string_args:
            validate_optional_string(group, arg, yaml_file)

        validate_empty(group, 'group', yaml_file)
