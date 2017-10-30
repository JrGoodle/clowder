# -*- coding: utf-8 -*-
"""clowder.yaml loading

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from termcolor import colored

import clowder.util.formatting as fmt


def load_yaml_base(parsed_yaml, combined_yaml):
    """Load clowder from base yaml file

    :param dict parsed_yaml: Parsed YAML python object
    :param dict combined_yaml: Combined YAML python object
    :return:
    """

    combined_yaml['defaults'] = parsed_yaml['defaults']
    if 'depth' not in parsed_yaml['defaults']:
        combined_yaml['defaults']['depth'] = 0
    combined_yaml['sources'] = parsed_yaml['sources']
    combined_yaml['groups'] = parsed_yaml['groups']


def load_yaml_import(parsed_yaml, combined_yaml):
    """Load clowder from import yaml file

    :param dict parsed_yaml: Parsed YAML python object
    :param dict combined_yaml: Combined YAML python object
    :return:
    """

    if 'defaults' in parsed_yaml:
        _load_yaml_import_defaults(parsed_yaml['defaults'], combined_yaml['defaults'])
    if 'sources' in parsed_yaml:
        _load_yaml_import_sources(parsed_yaml['sources'], combined_yaml['sources'])
    if 'groups' in parsed_yaml:
        _load_yaml_import_groups(parsed_yaml['groups'], combined_yaml['groups'])


def _load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group

    :param dict imported_defaults: Parsed YAML python object for imported defaults
    :param dict defaults: Parsed YAML python object for defaults
    :return:
    """

    args = ['depth', 'recursive', 'ref', 'remote', 'source', 'timestamp_author']
    for arg in args:
        _override_import_value(defaults, imported_defaults, arg)


def _load_yaml_import_groups(imported_groups, groups):
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
                args = ['depth', 'recursive', 'ref', 'remote', 'source', 'timestamp_author']
                for arg in args:
                    _override_import_value(group, imported_group, arg)
                if 'projects' in imported_group:
                    _load_yaml_import_projects(imported_group['projects'], group['projects'])
            combined_groups.append(group)
        groups = combined_groups


def _load_yaml_import_projects(imported_projects, projects):
    """Load clowder projects from imported group

    :param dict imported_projects: Parsed YAML python object for imported projects
    :param dict projects: Parsed YAML python object for projects
    :return:
    """

    project_names = [p['name'] for p in projects]
    for imported_project in imported_projects:
        if imported_project['name'] not in project_names:
            if 'path' not in imported_project:
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
            args = ['depth', 'fork', 'path', 'recursive', 'ref', 'remote', 'source', 'timestamp_author']
            for arg in args:
                _override_import_value(project, imported_project, arg)
            combined_projects.append(imported_project)
        projects = combined_projects


def _load_yaml_import_sources(imported_sources, sources):
    """Load clowder sources from imported yaml

    :param dict imported_sources: Parsed YAML python object for imported sources
    :param dict sources: Parsed YAML python object for sources
    :return:
    """

    source_names = [s['name'] for s in sources]
    for imported_source in imported_sources:
        if imported_source['name'] not in source_names:
            sources.append(imported_source)
            continue
        combined_sources = []
        for source in sources:
            if source.name == imported_source['name']:
                combined_sources.append(imported_source)
            else:
                combined_sources.append(source)
        sources = combined_sources


def _override_import_value(dictionary, imported_dictionary, value):
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param dict imported_dictionary: Imported parsed YAML python object
    :param str value: Name of entry to check
    :return:
    """

    if value in imported_dictionary:
        dictionary[value] = imported_dictionary[value]