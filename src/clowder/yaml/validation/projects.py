# -*- coding: utf-8 -*-
"""clowder.yaml projects validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from clowder.yaml.validation.forks import validate_yaml_fork
from clowder.yaml.validation.util import (
    validate_depth,
    validate_empty,
    validate_not_empty,
    validate_optional_ref,
    validate_optional_bool,
    validate_optional_string,
    validate_required_string,
    validate_type
)


def validate_yaml_projects_import(projects, yaml_file):
    """Validate projects in clowder loaded from yaml file import

    :param dict projects: Parsed YAML python object for projects
    :param str yaml_file: Path to yaml file
    """

    validate_type(projects, 'projects', list, 'list', yaml_file)
    validate_not_empty(projects, 'projects', yaml_file)

    for project in projects:
        validate_type(project, 'project', dict, 'dict', yaml_file)

        validate_not_empty(project, 'project', yaml_file)
        validate_required_string(project, 'project', 'name', yaml_file)
        validate_not_empty(project, 'project', yaml_file)

        validate_optional_string(project, 'path', yaml_file)
        _validate_yaml_project_optional(project, yaml_file)

        validate_empty(project, 'project', yaml_file)


def validate_yaml_projects(projects, yaml_file):
    """Validate projects in clowder loaded from yaml file

    :param dict projects: Parsed YAML python object for projects
    :param str yaml_file: Path to yaml file
    """

    validate_type(projects, 'projects', list, 'list', yaml_file)
    validate_not_empty(projects, 'projects', yaml_file)

    for project in projects:
        validate_type(project, 'project', dict, 'dict', yaml_file)
        validate_not_empty(project, 'project', yaml_file)

        validate_required_string(project, 'project', 'name', yaml_file)
        validate_required_string(project, 'project', 'path', yaml_file)

        _validate_yaml_project_optional(project, yaml_file)

        validate_empty(project, 'project', yaml_file)


def _validate_yaml_project_optional(project, yaml_file):
    """Validate optional args in project in clowder loaded from yaml file

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    """

    args = ['remote', 'source', 'timestamp_author']
    for arg in args:
        validate_optional_string(project, arg, yaml_file)

    validate_optional_bool(project, 'recursive', yaml_file)
    validate_optional_ref(project, yaml_file)

    validate_depth(project, yaml_file)

    if 'fork' in project:
        validate_yaml_fork(project['fork'], yaml_file)
        del project['fork']
