# -*- coding: utf-8 -*-
"""clowder.yaml loading

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from termcolor import colored

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.util.clowder_utils import get_clowder_yaml_import_path
from clowder.yaml import __MAX_IMPORT_DEPTH__
from clowder.yaml.parsing import parse_yaml


def load_yaml():
    """Load clowder from yaml file

    :raise ClowderYAMLError:
    """

    yaml_file = os.path.join(ROOT_DIR, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    imported_yaml_files = []
    combined_yaml = {}
    while True:
        if 'import' not in parsed_yaml:
            _load_yaml_base(parsed_yaml, combined_yaml)
            break

        imported_yaml_files.append(parsed_yaml)
        imported_yaml_file = get_clowder_yaml_import_path(parsed_yaml['import'])

        parsed_yaml = parse_yaml(imported_yaml_file)
        if len(imported_yaml_files) > __MAX_IMPORT_DEPTH__:
            raise ClowderYAMLError(fmt.recursive_import_error(__MAX_IMPORT_DEPTH__))

    for parsed_yaml in reversed(imported_yaml_files):
        _load_yaml_import(parsed_yaml, combined_yaml)

    return combined_yaml


def _load_yaml_base(parsed_yaml, combined_yaml):
    """Load clowder from base yaml file

    :param dict parsed_yaml: Parsed YAML python object
    :param dict combined_yaml: Combined YAML python object
    """

    combined_yaml['defaults'] = parsed_yaml['defaults']
    if 'depth' not in parsed_yaml['defaults']:
        combined_yaml['defaults']['depth'] = 0
    combined_yaml['sources'] = parsed_yaml['sources']
    combined_yaml['groups'] = parsed_yaml['groups']


def _load_yaml_import(parsed_yaml, combined_yaml):
    """Load clowder from import yaml file

    :param dict parsed_yaml: Parsed YAML python object
    :param dict combined_yaml: Combined YAML python object
    """

    if 'defaults' in parsed_yaml:
        _load_yaml_import_defaults(parsed_yaml['defaults'], combined_yaml['defaults'])
    if 'sources' in parsed_yaml:
        _load_yaml_import_sources(parsed_yaml['sources'], combined_yaml['sources'])
    if 'groups' in parsed_yaml:
        _load_yaml_import_groups(parsed_yaml['groups'], combined_yaml['groups'])


def _load_yaml_import_combine_group(imported_group, groups):
    """Combine imported group with existing groups

    :param dict imported_group: Parsed YAML python object for imported group
    :param list groups: Parsed YAML python object for groups
    :return: Combined groups
    :rtype: list
    """

    combined_groups = []
    for group in groups:
        if group['name'] != imported_group['name']:
            combined_groups.append(group)
            continue

        args = ['depth', 'recursive', 'ref', 'remote', 'source', 'timestamp_author']
        for arg in args:
            _override_import_value(group, imported_group, arg)
        if 'projects' in imported_group:
            _load_yaml_import_projects(imported_group['projects'], group['projects'])

    return combined_groups


def _load_yaml_import_combine_project(imported_project, projects):
    """Combine imported project with existing projects

    :param dict imported_project: Parsed YAML python object for imported project
    :param list projects: Parsed YAML python object for projects
    :return: Combined projects
    :rtype: list
    """

    combined_projects = []
    for project in projects:
        if project['name'] != imported_project['name']:
            combined_projects.append(project)
            continue

        args = ['depth', 'fork', 'path', 'recursive', 'ref', 'remote', 'source', 'timestamp_author']
        for arg in args:
            _override_import_value(project, imported_project, arg)
        combined_projects.append(imported_project)

    return combined_projects


def _load_yaml_import_combine_source(imported_source, sources):
    """Combine imported source with existing sources

    :param dict imported_source: Parsed YAML python object for imported source
    :param list sources: Parsed YAML python object for sources
    :return: Combined sources
    :rtype: list
    """

    combined_sources = []
    for source in sources:
        if source.name == imported_source['name']:
            combined_sources.append(imported_source)
        else:
            combined_sources.append(source)

    return combined_sources


def _load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group

    :param dict imported_defaults: Parsed YAML python object for imported defaults
    :param dict defaults: Parsed YAML python object for defaults
    """

    args = ['depth', 'recursive', 'ref', 'remote', 'source', 'timestamp_author', 'protocol']
    for arg in args:
        _override_import_value(defaults, imported_defaults, arg)


def _load_yaml_import_groups(imported_groups, groups):
    """Load clowder groups from imported yaml

    :param dict imported_groups: Parsed YAML python object for imported groups
    :param list groups: Parsed YAML python object for groups
    """

    group_names = [g['name'] for g in groups]
    for imported_group in imported_groups:
        if imported_group['name'] in group_names:
            groups = _load_yaml_import_combine_group(imported_group, groups)
            continue

        groups.append(imported_group)


def _load_yaml_import_projects(imported_projects, projects):
    """Load clowder projects from imported group

    :param dict imported_projects: Parsed YAML python object for imported projects
    :param list projects: Parsed YAML python object for projects
    :raise ClowderExit:
    """

    project_names = [p['name'] for p in projects]
    for imported_project in imported_projects:
        if imported_project['name'] in project_names:
            projects = _load_yaml_import_combine_project(imported_project, projects)
            continue

        if 'path' not in imported_project:
            error = colored(' - Missing path in new project', 'red')
            print(fmt.invalid_yaml_error())
            print(fmt.error(error))
            raise ClowderExit(1)

        projects.append(imported_project)


def _load_yaml_import_sources(imported_sources, sources):
    """Load clowder sources from imported yaml

    :param dict imported_sources: Parsed YAML python object for imported sources
    :param list sources: Parsed YAML python object for sources
    """

    source_names = [s['name'] for s in sources]
    for imported_source in imported_sources:
        if imported_source['name'] in source_names:
            sources = _load_yaml_import_combine_source(imported_source, sources)
            continue

        sources.append(imported_source)


def _override_import_value(dictionary, imported_dictionary, value):
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param dict imported_dictionary: Imported parsed YAML python object
    :param str value: Name of entry to check
    """

    if value in imported_dictionary:
        dictionary[value] = imported_dictionary[value]
