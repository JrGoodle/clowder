# -*- coding: utf-8 -*-
"""clowder.yaml projects validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    validate_not_empty,
    validate_optional_ref,
    validate_optional_bool,
    validate_optional_string,
    validate_required_string,
    validate_type,
    validate_type_depth
)
from clowder.yaml.validation.forks import validate_yaml_fork


def validate_yaml_import_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file with import

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(project, 'project', dict, 'dict', yaml_file)
    validate_not_empty(project, 'project', yaml_file)

    validate_required_string(project, 'project', 'name', yaml_file)

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    validate_optional_string(project, 'path', yaml_file)

    validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.unknown_entry_error('project', project, yaml_file)
        raise ClowderError(error)


def validate_yaml_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(project, 'project', dict, 'dict', yaml_file)
    validate_not_empty(project, 'project', yaml_file)

    validate_required_string(project, 'project', 'name', yaml_file)
    validate_required_string(project, 'project', 'path', yaml_file)

    validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.unknown_entry_error('project', project, yaml_file)
        raise ClowderError(error)


def validate_yaml_project_optional(project, yaml_file):
    """Validate optional args in project in clowder loaded from yaml file

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_optional_string(project, 'remote', yaml_file)
    validate_optional_bool(project, 'recursive', yaml_file)
    validate_optional_string(project, 'timestamp_author', yaml_file)
    validate_optional_string(project, 'source', yaml_file)

    validate_optional_ref(project, yaml_file)

    if 'depth' in project:
        validate_type_depth(project['depth'], yaml_file)
        del project['depth']

    if 'fork' in project:
        fork = project['fork']
        validate_yaml_fork(fork, yaml_file)
        del project['fork']


def validate_yaml_projects(projects, yaml_file, is_import):
    """Validate projects in clowder loaded from yaml file

    :param dict projects: Parsed YAML python object for projects
    :param str yaml_file: Path to yaml file
    :param bool is_import: Whether the clowder.yaml file is an imported file
    :return:
    :raise ClowderError:
    """

    validate_type(projects, 'projects', list, 'list', yaml_file)
    validate_not_empty(projects, 'projects', yaml_file)

    for project in projects:
        if is_import:
            validate_yaml_import_project(project, yaml_file)
        else:
            validate_yaml_project(project, yaml_file)
