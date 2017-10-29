# -*- coding: utf-8 -*-
"""clowder.yaml parsing and validation functionality

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import yaml
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError


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


def parse_yaml(yaml_file):
    """Parse yaml file

    :param str yaml_file: Path to yaml file
    :return: YAML python object
    :rtype: dict
    """

    if os.path.isfile(yaml_file):
        try:
            with open(yaml_file) as raw_file:
                parsed_yaml = yaml.safe_load(raw_file)
                if parsed_yaml is None:
                    print(fmt.invalid_yaml_error())
                    print(fmt.empty_yaml_error(yaml_file) + '\n')
                    sys.exit(1)
                return parsed_yaml
        except yaml.YAMLError:
            print(fmt.open_file_error(yaml_file))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        print('\n' + fmt.missing_yaml_error() + '\n')
        sys.exit(1)


def print_yaml(root_directory):
    """Print current clowder yaml

    :param str root_directory: Path to root directory containing clowder.yaml symlink
    :return:
    """

    yaml_file = os.path.join(root_directory, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    yaml_files = []
    while True:
        yaml_files.append(yaml_file)
        if 'import' not in parsed_yaml:
            break

        imported_yaml = parsed_yaml['import']
        if imported_yaml == 'default':
            yaml_file = os.path.join(root_directory, '.clowder', 'clowder.yaml')
        else:
            yaml_file = os.path.join(root_directory, '.clowder', 'versions', imported_yaml, 'clowder.yaml')
        parsed_yaml = parse_yaml(yaml_file)

    for yaml_file in yaml_files:
        if os.path.isfile(yaml_file):
            try:
                with open(yaml_file) as raw_file:
                    contents = raw_file.read()
                    print('-' * 80)
                    if os.path.islink(yaml_file):
                        path = fmt.symlink_target(yaml_file)
                        path = fmt.remove_prefix(path, root_directory)
                        path = fmt.remove_prefix(path, '/')
                        print('\n' + fmt.get_path('clowder.yaml') + ' -> ' + fmt.get_path(path) + '\n')
                    else:
                        path = fmt.remove_prefix(yaml_file, root_directory)
                        path = fmt.remove_prefix(path, '/')
                        print('\n' + fmt.get_path(path) + '\n')
                    print(contents)
            except IOError as err:
                print(fmt.open_file_error(yaml_file))
                print(err)
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)


def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param str yaml_file: Path to save yaml file
    :return:
    """

    if os.path.isfile(yaml_file):
        print(fmt.file_exists_error(yaml_file) + '\n')
        sys.exit(1)

    try:
        with open(yaml_file, 'w') as raw_file:
            print(" - Save yaml to file")
            yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        print(fmt.save_file_error(yaml_file))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def validate_yaml(yaml_file):
    """Validate clowder.yaml with no import

    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    _validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    if not parsed_yaml:
        error = fmt.empty_yaml_error(yaml_file)
        raise ClowderError(error)

    _clowder_yaml_contains_value(parsed_yaml, 'defaults', yaml_file)
    _validate_yaml_defaults(parsed_yaml['defaults'], yaml_file)
    del parsed_yaml['defaults']

    _clowder_yaml_contains_value(parsed_yaml, 'sources', yaml_file)
    _validate_yaml_sources(parsed_yaml['sources'], yaml_file)
    del parsed_yaml['sources']

    _clowder_yaml_contains_value(parsed_yaml, 'groups', yaml_file)
    _validate_yaml_groups(parsed_yaml['groups'], yaml_file)
    del parsed_yaml['groups']

    if parsed_yaml:
        error = fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)


def validate_yaml_import(yaml_file):
    """Validate clowder.yaml with an import

    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    parsed_yaml = parse_yaml(yaml_file)
    _validate_type(parsed_yaml, fmt.yaml_file('clowder.yaml'), dict, 'dict', yaml_file)

    _clowder_yaml_contains_value(parsed_yaml, 'import', yaml_file)
    _validate_type(parsed_yaml['import'], 'import', str, 'str', yaml_file)
    del parsed_yaml['import']

    if not parsed_yaml:
        error = fmt.empty_yaml_error(yaml_file)
        raise ClowderError(error)

    if 'defaults' in parsed_yaml:
        _validate_yaml_import_defaults(parsed_yaml['defaults'], yaml_file)
        del parsed_yaml['defaults']

    if 'sources' in parsed_yaml:
        _validate_yaml_sources(parsed_yaml['sources'], yaml_file)
        del parsed_yaml['sources']

    if 'groups' in parsed_yaml:
        _validate_yaml_import_groups(parsed_yaml['groups'], yaml_file)
        del parsed_yaml['groups']

    if parsed_yaml:
        error = fmt.unknown_entry_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)


def _clowder_yaml_contains_value(parsed_yaml, value, yaml_file):
    """Check whether yaml file contains value

    :param dict parsed_yaml: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if value not in parsed_yaml:
        error = fmt.missing_entry_error(value, fmt.yaml_file('clowder.yaml'), yaml_file)
        raise ClowderError(error)


def _dict_contains_value(dictionary, name, value, yaml_file):
    """Check whether yaml file contains value

    :param dict dictionary: Parsed YAML python object
    :param str name: Name of entry to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """
    if value not in dictionary:
        error = fmt.missing_entry_error(value, name, yaml_file)
        raise ClowderError(error)


def _load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group

    :param dict imported_defaults: Parsed YAML python object for imported defaults
    :param dict defaults: Parsed YAML python object for defaults
    :return:
    """

    if 'recursive' in imported_defaults:
        defaults['recursive'] = imported_defaults['recursive']
    if 'ref' in imported_defaults:
        defaults['ref'] = imported_defaults['ref']
    if 'remote' in imported_defaults:
        defaults['remote'] = imported_defaults['remote']
    if 'source' in imported_defaults:
        defaults['source'] = imported_defaults['source']
    if 'depth' in imported_defaults:
        defaults['depth'] = imported_defaults['depth']
    if 'timestamp_author' in imported_defaults:
        defaults['timestamp_author'] = imported_defaults['timestamp_author']


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


def _validate_optional_ref(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    """
    if 'ref' in dictionary:
        _validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
        _validate_ref_type(dictionary, yaml_file)
        del dictionary['ref']


def _valid_ref_type(ref):
    """Validate that ref is formatted correctly

    :param str ref: Ref string requiring format 'refs/heads/<branch>', 'refs/tags/<tag>', or 40 character commit sha
    :return: True, if ref is properly formatted
    :rtype: bool
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return True
    elif ref.startswith(git_tag):
        return True
    elif len(ref) == 40:
        return True
    return False


def _validate_ref_type(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """
    if not _valid_ref_type(dictionary['ref']):
        error = fmt.invalid_ref_error(dictionary['ref'], yaml_file)
        raise ClowderError(error)


def _validate_type_depth(value, yaml_file):
    """Validate depth value

    :param int value: Integer depth value
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    error = fmt.depth_error(value, yaml_file)
    if not isinstance(value, int):
        raise ClowderError(error)
    if int(value) < 0:
        raise ClowderError(error)


def _validate_type(value, name, classinfo, type_name, yaml_file):
    """Validate value type

    :param value: Value to check
    :param str name: Name of value to print if invalid
    :param type classinfo: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if not isinstance(value, classinfo):
        error = fmt.type_error(name, yaml_file, type_name)
        raise ClowderError(error)


def _validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    if 'recursive' in defaults:
        _validate_type(defaults['recursive'], 'recursive', bool, 'bool', yaml_file)
        del defaults['recursive']

    _validate_optional_ref(defaults, yaml_file)

    if 'remote' in defaults:
        _validate_type(defaults['remote'], 'remote', str, 'str', yaml_file)
        del defaults['remote']

    if 'source' in defaults:
        _validate_type(defaults['source'], 'source', str, 'str', yaml_file)
        del defaults['source']

    if 'depth' in defaults:
        _validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'timestamp_author' in defaults:
        _validate_type(defaults['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del defaults['timestamp_author']

    if defaults:
        error = fmt.unknown_entry_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def _validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(defaults, 'defaults', dict, 'dict', yaml_file)
    if not defaults:
        error = fmt.missing_entries_error('defaults', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(defaults, 'defaults', 'ref', yaml_file)
    _validate_type(defaults['ref'], 'ref', str, 'str', yaml_file)
    _validate_ref_type(defaults, yaml_file)
    del defaults['ref']

    _dict_contains_value(defaults, 'defaults', 'remote', yaml_file)
    _validate_type(defaults['remote'], 'remote', str, 'str', yaml_file)
    del defaults['remote']

    _dict_contains_value(defaults, 'defaults', 'source', yaml_file)
    _validate_type(defaults['source'], 'source', str, 'str', yaml_file)
    del defaults['source']

    _validate_yaml_defaults_optional(defaults, yaml_file)

    if defaults:
        error = fmt.unknown_entry_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def _validate_yaml_defaults_optional(defaults, yaml_file):
    """Validate defaults optional args in clowder loaded from yaml file

    :param dict defaults: Parsed YAML python object for defaults
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if 'depth' in defaults:
        _validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'recursive' in defaults:
        _validate_type(defaults['recursive'], 'recursive', bool, 'bool', yaml_file)
        del defaults['recursive']

    if 'timestamp_author' in defaults:
        _validate_type(defaults['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del defaults['timestamp_author']


def _validate_yaml_fork(fork, yaml_file):
    """Validate fork in clowder loaded from yaml file

    :param dict fork: Parsed YAML python object for fork
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(fork, 'fork', dict, 'dict', yaml_file)

    if not fork:
        error = fmt.missing_entries_error('fork', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(fork, 'fork', 'name', yaml_file)
    _validate_type(fork['name'], 'name', str, 'str', yaml_file)
    del fork['name']

    _dict_contains_value(fork, 'fork', 'remote', yaml_file)
    _validate_type(fork['remote'], 'remote', str, 'str', yaml_file)
    del fork['remote']

    if fork:
        error = fmt.unknown_entry_error('fork', fork, yaml_file)
        raise ClowderError(error)


def _validate_yaml_import_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file with import

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(groups, 'groups', list, 'list', yaml_file)

    if not groups:
        error = fmt.missing_entries_error('groups', yaml_file)
        raise ClowderError(error)

    for group in groups:
        _validate_yaml_import_group(group, yaml_file)


def _validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file

    :param dict groups: Parsed YAML python object for groups
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(groups, 'groups', list, 'list', yaml_file)

    if not groups:
        error = fmt.missing_entries_error('groups', yaml_file)
        raise ClowderError(error)

    for group in groups:
        _validate_yaml_group(group, yaml_file)


def _validate_yaml_import_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file with import

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(project, 'project', dict, 'dict', yaml_file)

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(project, 'project', 'name', yaml_file)
    _validate_type(project['name'], 'name', str, 'str', yaml_file)
    del project['name']

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    if 'path' in project:
        _validate_type(project['path'], 'path', str, 'str', yaml_file)
        del project['path']

    _validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.unknown_entry_error('project', project, yaml_file)
        raise ClowderError(error)


def _validate_yaml_import_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file with import

    :param dict group: Parsed YAML python object for group
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(group, 'group', dict, 'dict', yaml_file)

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(group, 'group', 'name', yaml_file)
    _validate_type(group['name'], 'name', str, 'str', yaml_file)
    del group['name']

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    if 'projects' in group:
        _validate_yaml_projects(group['projects'], yaml_file, is_import=True)
        del group['projects']

    if 'recursive' in group:
        _validate_type(group['recursive'], 'recursive', bool, 'bool', yaml_file)
        del group['recursive']

    _validate_optional_ref(group, yaml_file)

    if 'remote' in group:
        _validate_type(group['remote'], 'remote', str, 'str', yaml_file)
        del group['remote']

    if 'source' in group:
        _validate_type(group['source'], 'source', str, 'str', yaml_file)
        del group['source']

    if 'depth' in group:
        _validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if 'timestamp_author' in group:
        _validate_type(group['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del group['timestamp_author']

    if group:
        error = fmt.unknown_entry_error('group', group, yaml_file)
        raise ClowderError(error)


def _validate_yaml_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file

    :param dict group: Parsed YAML python object for group
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(group, 'group', dict, 'dict', yaml_file)

    if not group:
        error = fmt.missing_entries_error('group', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(group, 'group', 'name', yaml_file)
    _validate_type(group['name'], 'name', str, 'str', yaml_file)
    del group['name']

    _dict_contains_value(group, 'group', 'projects', yaml_file)
    _validate_yaml_projects(group['projects'], yaml_file, is_import=False)
    del group['projects']

    if 'recursive' in group:
        _validate_type(group['recursive'], 'recursive', bool, 'bool', yaml_file)
        del group['recursive']

    if 'timestamp_author' in group:
        _validate_type(group['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del group['timestamp_author']

    _validate_optional_ref(group, yaml_file)

    if 'remote' in group:
        _validate_type(group['remote'], 'remote', str, 'str', yaml_file)
        del group['remote']

    if 'source' in group:
        _validate_type(group['source'], 'source', str, 'str', yaml_file)
        del group['source']

    if 'depth' in group:
        _validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if group:
        error = fmt.unknown_entry_error('group', group, yaml_file)
        raise ClowderError(error)


def _validate_yaml_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(project, 'project', dict, 'dict', yaml_file)

    if not project:
        error = fmt.missing_entries_error('project', yaml_file)
        raise ClowderError(error)

    _dict_contains_value(project, 'project', 'name', yaml_file)
    _validate_type(project['name'], 'name', str, 'str', yaml_file)
    del project['name']

    _dict_contains_value(project, 'project', 'path', yaml_file)
    _validate_type(project['path'], 'path', str, 'str', yaml_file)
    del project['path']

    _validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.unknown_entry_error('project', project, yaml_file)
        raise ClowderError(error)


def _validate_yaml_project_optional(project, yaml_file):
    """Validate optional args in project in clowder loaded from yaml file

    :param dict project: Parsed YAML python object for project
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if 'remote' in project:
        _validate_type(project['remote'], 'remote', str, 'str', yaml_file)
        del project['remote']

    if 'recursive' in project:
        _validate_type(project['recursive'], 'recursive', bool, 'bool', yaml_file)
        del project['recursive']

    if 'timestamp_author' in project:
        _validate_type(project['timestamp_author'], 'timestamp_author', str, 'str', yaml_file)
        del project['timestamp_author']

    _validate_optional_ref(project, yaml_file)

    if 'source' in project:
        _validate_type(project['source'], 'source', str, 'str', yaml_file)
        del project['source']

    if 'depth' in project:
        _validate_type_depth(project['depth'], yaml_file)
        del project['depth']

    if 'fork' in project:
        fork = project['fork']
        _validate_yaml_fork(fork, yaml_file)
        del project['fork']


def _validate_yaml_projects(projects, yaml_file, is_import):
    """Validate projects in clowder loaded from yaml file

    :param dict projects: Parsed YAML python object for projects
    :param str yaml_file: Path to yaml file
    :param bool is_import: Whether the clowder.yaml file is an imported file
    :return:
    :raise ClowderError:
    """

    _validate_type(projects, 'projects', list, 'list', yaml_file)
    if not projects:
        error = fmt.missing_entries_error('projects', yaml_file)
        raise ClowderError(error)

    for project in projects:
        if is_import:
            _validate_yaml_import_project(project, yaml_file)
        else:
            _validate_yaml_project(project, yaml_file)


def _validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file

    :param dict sources: Parsed YAML python object for sources
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    _validate_type(sources, 'sources', list, 'list', yaml_file)
    if not sources:
        error = fmt.missing_entries_error('sources', yaml_file)
        raise ClowderError(error)

    for source in sources:
        _validate_type(source, 'source', dict, 'dict', yaml_file)
        if not source:
            error = fmt.missing_entries_error('source', yaml_file)
            raise ClowderError(error)

        _dict_contains_value(source, 'source', 'name', yaml_file)
        _validate_type(source['name'], 'name', str, 'str', yaml_file)
        del source['name']

        _dict_contains_value(source, 'source', 'url', yaml_file)
        _validate_type(source['url'], 'url', str, 'str', yaml_file)
        del source['url']

        if source:
            error = fmt.unknown_entry_error('source', source, yaml_file)
            raise ClowderError(error)
