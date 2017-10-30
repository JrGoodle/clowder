# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    dict_contains_value,
    validate_optional_ref,
    validate_type,
    validate_type_depth
)
from clowder.yaml.validation.forks import validate_yaml_fork


def load_yaml_import_projects(imported_projects, projects):
    """Load clowder projects from imported group

    :param dict imported_projects: Parsed YAML python object for imported projects
    :param dict projects: Parsed YAML python object for projects
    :return:
    """

    project_names = [p['name'] for p in projects]
    for imported_project in imported_projects:
        if imported_project['name'] not in project_names:
            if 'path' not in imported_project:
                # error = fmt.invalid_entries_error('defaults', defaults, yaml_file)
                error = colored(' - Missing path in new project', 'red')
                print(fmt.invalid_yaml_error())
                print(fmt.error(error))
                sys.exit(1)
            projects.append(imported_project)
            continue
        combined_projects = []
        for project in projects:
            if project['name'] != imported_project['name']:
                combined_projects.append(project)
                continue
            if 'path' in imported_project:
                project['path'] = imported_project['path']
            if 'depth' in imported_project:
                project['depth'] = imported_project['depth']
            if 'timestamp_author' in imported_project:
                project['timestamp_author'] = imported_project['timestamp_author']
            if 'recursive' in imported_project:
                project['recursive'] = imported_project['recursive']
            if 'ref' in imported_project:
                project['ref'] = imported_project['ref']
            if 'remote' in imported_project:
                project['remote'] = imported_project['remote']
            if 'fork' in imported_project:
                project['fork'] = imported_project['fork']
            if 'source' in imported_project:
                project['source'] = imported_project['source']['name']
            combined_projects.append(imported_project)
        projects = combined_projects


def validate_yaml_import_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file with import

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(project, 'project', dict, 'dict', yaml_file)

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    dict_contains_value(project, 'project', 'name', yaml_file)
    validate_type(project['name'], 'name', str, 'str', yaml_file)
    del project['name']

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    if 'path' in project:
        validate_type(project['path'], 'path', str, 'str', yaml_file)
        del project['path']

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

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    dict_contains_value(project, 'project', 'name', yaml_file)
    validate_type(project['name'], 'name', str, 'str', yaml_file)
    del project['name']

    dict_contains_value(project, 'project', 'path', yaml_file)
    validate_type(project['path'], 'path', str, 'str', yaml_file)
    del project['path']

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

    if 'remote' in project:
        validate_type(project['remote'], 'remote', str, 'str', yaml_file)
        del project['remote']

    if 'recursive' in project:
        validate_type(project['recursive'], 'recursive', bool, 'bool', yaml_file)
        del project['recursive']

    if 'timestamp_author' in project:
        validate_type(project['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del project['timestamp_author']

    validate_optional_ref(project, yaml_file)

    if 'source' in project:
        validate_type(project['source'], 'source', str, 'str', yaml_file)
        del project['source']

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
    if not projects:
        error = fmt.missing_entries_error('projects', yaml_file)
        raise ClowderError(error)

    for project in projects:
        if is_import:
            validate_yaml_import_project(project, yaml_file)
        else:
            validate_yaml_project(project, yaml_file)
