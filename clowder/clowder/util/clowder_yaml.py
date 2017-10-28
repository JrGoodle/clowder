"""clowder.yaml parsing and functionality"""

from __future__ import print_function

import os
import sys

import yaml
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError


def _clowder_yaml_contains_value(parsed_yaml, value, yaml_file):
    """Check whether yaml file contains value"""
    if value not in parsed_yaml:
        error = fmt.missing_entry_error(value, fmt.yaml_file('clowder.yaml'), yaml_file)
        raise ClowderError(error)


def _dict_contains_value(dictionary, name, value, yaml_file):
    """Check whether yaml file contains value"""
    if value not in dictionary:
        error = fmt.missing_entry_error(value, name, yaml_file)
        raise ClowderError(error)


def load_yaml_base(parsed_yaml, combined_yaml):
    """Load clowder from base yaml file"""

    combined_yaml['defaults'] = parsed_yaml['defaults']
    if 'depth' not in parsed_yaml['defaults']:
        combined_yaml['defaults']['depth'] = 0
    combined_yaml['sources'] = parsed_yaml['sources']
    combined_yaml['groups'] = parsed_yaml['groups']


def load_yaml_import(parsed_yaml, combined_yaml):
    """Load clowder from import yaml file"""

    if 'defaults' in parsed_yaml:
        _load_yaml_import_defaults(parsed_yaml['defaults'], combined_yaml['defaults'])
    if 'sources' in parsed_yaml:
        _load_yaml_import_sources(parsed_yaml['sources'], combined_yaml['sources'])
    if 'groups' in parsed_yaml:
        _load_yaml_import_groups(parsed_yaml['groups'], combined_yaml['groups'])


def parse_yaml(yaml_file):
    """Parse yaml file"""

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
            fmt.open_file_error(yaml_file)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
    else:
        print()
        print(fmt.missing_yaml_error())
        print()
        sys.exit(1)


def print_yaml(root_directory):
    """Print current clowder yaml"""

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
                        print()
                        print(fmt.get_path('clowder.yaml') + ' -> ' + fmt.get_path(path))
                        print()
                    else:
                        path = fmt.remove_prefix(yaml_file, root_directory)
                        path = fmt.remove_prefix(path, '/')
                        print('\n' + fmt.get_path(path) + '\n')
                    print(contents)
            except IOError as err:
                fmt.open_file_error(yaml_file)
                print(err)
                sys.exit(1)
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)


def save_yaml(yaml_output, yaml_file):
    """Save yaml file to disk"""

    if os.path.isfile(yaml_file):
        fmt.file_exists_error(yaml_file)
        print()
        sys.exit(1)

    try:
        with open(yaml_file, 'w') as raw_file:
            print(" - Save yaml to file")
            yaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        fmt.save_file_error(yaml_file)
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def validate_yaml(yaml_file):
    """Validate clowder.yaml with no import"""

    parsed_yaml = parse_yaml(yaml_file)
    _validate_type_dict(parsed_yaml, fmt.yaml_file('clowder.yaml'), yaml_file)

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
        error = fmt.invalid_entries_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)


def validate_yaml_import(yaml_file):
    """Validate clowder.yaml with an import"""

    parsed_yaml = parse_yaml(yaml_file)
    _validate_type_dict(parsed_yaml, fmt.yaml_file('clowder.yaml'), yaml_file)

    _clowder_yaml_contains_value(parsed_yaml, 'import', yaml_file)
    _validate_type_str(parsed_yaml['import'], 'import', yaml_file)
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
        error = fmt.invalid_entries_error(fmt.yaml_file('clowder.yaml'), parsed_yaml, yaml_file)
        raise ClowderError(error)


def _load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group"""

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
    """Load clowder groups from import yaml"""

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
    """Load clowder projects from imported group"""

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
    """Load clowder sources from import yaml"""

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


def _valid_ref_type(ref):
    """Validate that ref is formatted correctly"""

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return True
    elif ref.startswith(git_tag):
        return True
    elif len(ref) == 40:
        return True
    return False


def _validate_ref_type(dictionary, value, yaml_file):
    """Check whether ref type is valid"""
    if not _valid_ref_type(dictionary[value]):
        error = fmt.invalid_ref_error(dictionary[value], yaml_file)
        raise ClowderError(error)


def _validate_type_bool(value, name, yaml_file):
    """Validate value is a bool"""

    if not isinstance(value, bool):
        error = fmt.not_bool_error(name, yaml_file)
        raise ClowderError(error)


def _validate_type_depth(value, yaml_file):
    """Validate depth value"""

    error = fmt.depth_error(value, yaml_file)
    if not isinstance(value, int):
        raise ClowderError(error)
    if int(value) < 0:
        raise ClowderError(error)


def _validate_type_dict(value, name, yaml_file):
    """Validate value is a dict"""

    if not isinstance(value, dict):
        error = fmt.not_dictionary_error(name, yaml_file)
        raise ClowderError(error)


def _validate_type_list(value, name, yaml_file):
    """Validate value is a list"""

    if not isinstance(value, list):
        error = fmt.not_list_error(name, yaml_file)
        raise ClowderError(error)


def _validate_type_str(value, name, yaml_file):
    """Validate value is a str"""

    if not isinstance(value, str):
        error = fmt.not_string_error(name, yaml_file)
        raise ClowderError(error)


def _validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import"""

    _validate_type_dict(defaults, 'defaults', yaml_file)
    if 'recursive' in defaults:
        _validate_type_bool(defaults['recursive'], 'recursive', yaml_file)
        del defaults['recursive']

    if 'ref' in defaults:
        _validate_type_str(defaults['ref'], 'ref', yaml_file)
        _validate_ref_type(defaults, 'ref', yaml_file)
        del defaults['ref']

    if 'remote' in defaults:
        _validate_type_str(defaults['remote'], 'remote', yaml_file)
        del defaults['remote']

    if 'source' in defaults:
        _validate_type_str(defaults['source'], 'source', yaml_file)
        del defaults['source']

    if 'depth' in defaults:
        _validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'timestamp_author' in defaults:
        _validate_type_str(defaults['timestamp_author'], 'timestamp_author', yaml_file)
        del defaults['timestamp_author']

    if defaults:
        error = fmt.invalid_entries_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def _validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file"""

    _validate_type_dict(defaults, 'defaults', yaml_file)
    if not defaults:
        error = fmt.invalid_entries_error('defaults', defaults, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(defaults, 'defaults', 'ref', yaml_file)
    _validate_type_str(defaults['ref'], 'ref', yaml_file)
    _validate_ref_type(defaults, 'ref', yaml_file)
    del defaults['ref']

    _dict_contains_value(defaults, 'defaults', 'remote', yaml_file)
    _validate_type_str(defaults['remote'], 'remote', yaml_file)
    del defaults['remote']

    _dict_contains_value(defaults, 'defaults', 'source', yaml_file)
    _validate_type_str(defaults['source'], 'source', yaml_file)
    del defaults['source']

    _validate_yaml_defaults_optional(defaults, yaml_file)

    if defaults:
        error = fmt.invalid_entries_error('defaults', defaults, yaml_file)
        raise ClowderError(error)


def _validate_yaml_defaults_optional(defaults, yaml_file):
    """Validate defaults optional args in clowder loaded from yaml file"""

    if 'depth' in defaults:
        _validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'recursive' in defaults:
        _validate_type_bool(defaults['recursive'], 'recursive', yaml_file)
        del defaults['recursive']

    if 'timestamp_author' in defaults:
        _validate_type_str(defaults['timestamp_author'], 'timestamp_author', yaml_file)
        del defaults['timestamp_author']


def _validate_yaml_fork(fork, yaml_file):
    """Validate fork in clowder loaded from yaml file"""

    _validate_type_dict(fork, 'fork', yaml_file)

    if not fork:
        error = fmt.invalid_entries_error('fork', fork, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(fork, 'fork', 'name', yaml_file)
    _validate_type_str(fork['name'], 'name', yaml_file)
    del fork['name']

    _dict_contains_value(fork, 'fork', 'remote', yaml_file)
    _validate_type_str(fork['remote'], 'remote', yaml_file)
    del fork['remote']

    if fork:
        error = fmt.invalid_entries_error('fork', fork, yaml_file)
        raise ClowderError(error)


def _validate_yaml_import_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file with import"""

    _validate_type_list(groups, 'groups', yaml_file)

    if not groups:
        error = fmt.invalid_entries_error('groups', groups, yaml_file)
        raise ClowderError(error)

    for group in groups:
        _validate_yaml_import_group(group, yaml_file)


def _validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file"""

    _validate_type_list(groups, 'groups', yaml_file)

    if not groups:
        error = fmt.invalid_entries_error('groups', groups, yaml_file)
        raise ClowderError(error)

    for group in groups:
        _validate_yaml_group(group, yaml_file)


def _validate_yaml_import_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file with import"""

    _validate_type_dict(project, 'project', yaml_file)

    if not project:
        error = fmt.invalid_entries_error('project', project, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(project, 'project', 'name', yaml_file)
    _validate_type_str(project['name'], 'name', yaml_file)
    del project['name']

    if not project:
        error = fmt.invalid_entries_error('project', project, yaml_file)
        raise ClowderError(error)

    if 'path' in project:
        _validate_type_str(project['path'], 'path', yaml_file)
        del project['path']

    _validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.invalid_entries_error('project', project, yaml_file)
        raise ClowderError(error)


def _validate_yaml_import_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file with import"""

    _validate_type_dict(group, 'group', yaml_file)

    if not group:
        error = fmt.invalid_entries_error('group', group, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(group, 'group', 'name', yaml_file)
    _validate_type_str(group['name'], 'name', yaml_file)
    del group['name']

    if not group:
        error = fmt.invalid_entries_error('group', group, yaml_file)
        raise ClowderError(error)

    if 'projects' in group:
        _validate_yaml_projects(group['projects'], yaml_file, is_import=True)
        del group['projects']

    if 'recursive' in group:
        _validate_type_bool(group['recursive'], 'recursive', yaml_file)
        del group['recursive']

    if 'ref' in group:
        _validate_type_str(group['ref'], 'ref', yaml_file)
        _validate_ref_type(group, 'ref', yaml_file)
        del group['ref']

    if 'remote' in group:
        _validate_type_str(group['remote'], 'remote', yaml_file)
        del group['remote']

    if 'source' in group:
        _validate_type_str(group['source'], 'source', yaml_file)
        del group['source']

    if 'depth' in group:
        _validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if 'timestamp_author' in group:
        _validate_type_str(group['timestamp_author'], 'timestamp_author', yaml_file)
        del group['timestamp_author']

    if group:
        error = fmt.invalid_entries_error('group', group, yaml_file)
        raise ClowderError(error)


def _validate_yaml_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file"""

    _validate_type_dict(group, 'group', yaml_file)

    if not group:
        error = fmt.invalid_entries_error('group', group, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(group, 'group', 'name', yaml_file)
    _validate_type_str(group['name'], 'name', yaml_file)
    del group['name']

    _dict_contains_value(group, 'group', 'projects', yaml_file)
    _validate_yaml_projects(group['projects'], yaml_file, is_import=False)
    del group['projects']

    if 'recursive' in group:
        _validate_type_bool(group['recursive'], 'recursive', yaml_file)
        del group['recursive']

    if 'timestamp_author' in group:
        _validate_type_str(group['timestamp_author'], 'timestamp_author', yaml_file)
        del group['timestamp_author']

    if 'ref' in group:
        _validate_type_str(group['ref'], 'ref', yaml_file)
        _validate_ref_type(group, 'ref', yaml_file)
        del group['ref']

    if 'remote' in group:
        _validate_type_str(group['remote'], 'remote', yaml_file)
        del group['remote']

    if 'source' in group:
        _validate_type_str(group['source'], 'source', yaml_file)
        del group['source']

    if 'depth' in group:
        _validate_type_depth(group['depth'], yaml_file)
        del group['depth']

    if group:
        error = fmt.invalid_entries_error('group', group, yaml_file)
        raise ClowderError(error)


def _validate_yaml_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file"""

    _validate_type_dict(project, 'project', yaml_file)

    if not project:
        error = fmt.invalid_entries_error('project', project, yaml_file)
        raise ClowderError(error)

    _dict_contains_value(project, 'project', 'name', yaml_file)
    _validate_type_str(project['name'], 'name', yaml_file)
    del project['name']

    _dict_contains_value(project, 'project', 'path', yaml_file)
    _validate_type_str(project['path'], 'path', yaml_file)
    del project['path']

    _validate_yaml_project_optional(project, yaml_file)

    if project:
        error = fmt.invalid_entries_error('project', project, yaml_file)
        raise ClowderError(error)


def _validate_yaml_project_optional(project, yaml_file):
    """Validate optional args in project in clowder loaded from yaml file"""

    if 'remote' in project:
        _validate_type_str(project['remote'], 'remote', yaml_file)
        del project['remote']

    if 'recursive' in project:
        _validate_type_bool(project['recursive'], 'recursive', yaml_file)
        del project['recursive']

    if 'timestamp_author' in project:
        _validate_type_str(project['timestamp_author'], 'timestamp_author', yaml_file)
        del project['timestamp_author']

    if 'ref' in project:
        _validate_type_str(project['ref'], 'ref', yaml_file)
        _validate_ref_type(project, 'ref', yaml_file)
        del project['ref']

    if 'source' in project:
        _validate_type_str(project['source'], 'source', yaml_file)
        del project['source']

    if 'depth' in project:
        _validate_type_depth(project['depth'], yaml_file)
        del project['depth']

    if 'fork' in project:
        fork = project['fork']
        _validate_yaml_fork(fork, yaml_file)
        del project['fork']


def _validate_yaml_projects(projects, yaml_file, is_import):
    """Validate projects in clowder loaded from yaml file"""

    _validate_type_list(projects, 'projects', yaml_file)
    if not projects:
        error = fmt.invalid_entries_error('projects', projects, yaml_file)
        raise ClowderError(error)

    for project in projects:
        if is_import:
            _validate_yaml_import_project(project, yaml_file)
        else:
            _validate_yaml_project(project, yaml_file)


def _validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file"""

    _validate_type_list(sources, 'sources', yaml_file)
    if not sources:
        error = fmt.invalid_entries_error('sources', sources, yaml_file)
        raise ClowderError(error)

    for source in sources:
        _validate_type_dict(source, 'source', yaml_file)
        if not source:
            error = fmt.invalid_entries_error('source', source, yaml_file)
            raise ClowderError(error)

        _dict_contains_value(source, 'source', 'name', yaml_file)
        _validate_type_str(source['name'], 'name', yaml_file)
        del source['name']

        _dict_contains_value(source, 'source', 'url', yaml_file)
        _validate_type_str(source['url'], 'url', yaml_file)
        del source['url']

        if source:
            error = fmt.invalid_entries_error('source', source, yaml_file)
            raise ClowderError(error)
