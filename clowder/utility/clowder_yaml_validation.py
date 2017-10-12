"""Clowder yaml validation"""

import sys
from clowder.utility.clowder_utilities import parse_yaml
from clowder.utility.print_utilities import (
    format_depth_error,
    format_empty_yaml_error,
    format_invalid_entries_error,
    format_missing_entry_error,
    format_not_bool_error,
    format_not_dictionary_error,
    format_not_list_error,
    format_not_string_error,
    format_invalid_ref_error,
    format_yaml_file,
    print_error,
    print_invalid_yaml_error
)


def validate_yaml(yaml_file):
    """Validate clowder.yaml with no import"""
    parsed_yaml = parse_yaml(yaml_file)
    try:
        _validate_type_dict(parsed_yaml, format_yaml_file('clowder.yaml'), yaml_file)
        if not parsed_yaml:
            error = format_empty_yaml_error(yaml_file)
            raise Exception(error)

        if 'defaults' not in parsed_yaml:
            error = format_missing_entry_error('defaults',
                                               format_yaml_file('clowder.yaml'),
                                               yaml_file)
            raise Exception(error)
        validate_yaml_defaults(parsed_yaml['defaults'], yaml_file)
        del parsed_yaml['defaults']

        if 'sources' not in parsed_yaml:
            error = format_missing_entry_error('sources',
                                               format_yaml_file('clowder.yaml'),
                                               yaml_file)
            raise Exception(error)
        validate_yaml_sources(parsed_yaml['sources'], yaml_file)
        del parsed_yaml['sources']

        if 'groups' not in parsed_yaml:
            error = format_missing_entry_error('groups',
                                               format_yaml_file('clowder.yaml'),
                                               yaml_file)
            raise Exception(error)
        validate_yaml_groups(parsed_yaml['groups'], yaml_file)
        del parsed_yaml['groups']

        if parsed_yaml:
            error = format_invalid_entries_error(format_yaml_file('clowder.yaml'),
                                                 parsed_yaml, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_import(yaml_file):
    """Validate clowder.yaml with an import"""
    parsed_yaml = parse_yaml(yaml_file)
    try:
        _validate_type_dict(parsed_yaml, format_yaml_file('clowder.yaml'), yaml_file)
        if 'import' not in parsed_yaml:
            error = format_missing_entry_error('import',
                                               format_yaml_file('clowder.yaml'),
                                               yaml_file)
            raise Exception(error)
        _validate_type_str(parsed_yaml['import'], 'import', yaml_file)
        del parsed_yaml['import']

        if not parsed_yaml:
            error = format_empty_yaml_error(yaml_file)
            raise Exception(error)

        if 'defaults' in parsed_yaml:
            validate_yaml_import_defaults(parsed_yaml['defaults'], yaml_file)
            del parsed_yaml['defaults']

        if 'sources' in parsed_yaml:
            validate_yaml_sources(parsed_yaml['sources'], yaml_file)
            del parsed_yaml['sources']

        if 'groups' in parsed_yaml:
            validate_yaml_import_groups(parsed_yaml['groups'], yaml_file)
            del parsed_yaml['groups']

        if parsed_yaml:
            error = format_invalid_entries_error(format_yaml_file('clowder.yaml'),
                                                 parsed_yaml, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_import_defaults(defaults, yaml_file):
    """Validate clowder.yaml defaults with an import"""
    _validate_type_dict(defaults, 'defaults', yaml_file)
    if 'recursive' in defaults:
        _validate_type_bool(defaults['recursive'], 'recursive', yaml_file)
        del defaults['recursive']
    if 'ref' in defaults:
        _validate_type_str(defaults['ref'], 'ref', yaml_file)
        if not _valid_ref_type(defaults['ref']):
            error = format_invalid_ref_error(defaults['ref'], yaml_file)
            raise Exception(error)
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
    if defaults:
        error = format_invalid_entries_error('defaults', defaults, yaml_file)
        raise Exception(error)


def validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        _validate_type_dict(defaults, 'defaults', yaml_file)
        if not defaults:
            error = format_invalid_entries_error('defaults', defaults, yaml_file)
            raise Exception(error)

        if 'ref' not in defaults:
            error = format_missing_entry_error('ref', 'defaults', yaml_file)
            raise Exception(error)
        _validate_type_str(defaults['ref'], 'ref', yaml_file)
        if not _valid_ref_type(defaults['ref']):
            error = format_invalid_ref_error(defaults['ref'], yaml_file)
            raise Exception(error)
        del defaults['ref']

        if 'remote' not in defaults:
            error = format_missing_entry_error('remote', 'defaults', yaml_file)
            raise Exception(error)
        _validate_type_str(defaults['remote'], 'remote', yaml_file)
        del defaults['remote']

        if 'source' not in defaults:
            error = format_missing_entry_error('source', 'defaults', yaml_file)
            raise Exception(error)
        _validate_type_str(defaults['source'], 'source', yaml_file)
        del defaults['source']

        validate_yaml_defaults_optional(defaults, yaml_file)

        if defaults:
            error = format_invalid_entries_error('defaults', defaults, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_defaults_optional(defaults, yaml_file):
    """Validate defaults optional args in clowder loaded from yaml file"""
    if 'depth' in defaults:
        _validate_type_depth(defaults['depth'], yaml_file)
        del defaults['depth']

    if 'recursive' in defaults:
        _validate_type_bool(defaults['recursive'], 'recursive', yaml_file)
        del defaults['recursive']


def validate_yaml_fork(fork, yaml_file):
    """Validate fork in clowder loaded from yaml file"""
    try:
        _validate_type_dict(fork, 'fork', yaml_file)
        if not fork:
            error = format_invalid_entries_error('fork', fork, yaml_file)
            raise Exception(error)

        if 'name' not in fork:
            error = format_missing_entry_error('name', 'fork', yaml_file)
            raise Exception(error)
        _validate_type_str(fork['name'], 'name', yaml_file)
        del fork['name']

        if 'remote' not in fork:
            error = format_missing_entry_error('remote', 'fork', yaml_file)
            raise Exception(error)
        _validate_type_str(fork['remote'], 'remote', yaml_file)
        del fork['remote']

        if fork:
            error = format_invalid_entries_error('fork', fork, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_import_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file with import"""
    try:
        _validate_type_list(groups, 'groups', yaml_file)
        if not groups:
            error = format_invalid_entries_error('groups', groups, yaml_file)
            raise Exception(error)

        for group in groups:
            validate_yaml_import_group(group, yaml_file)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file"""
    try:
        _validate_type_list(groups, 'groups', yaml_file)
        if not groups:
            error = format_invalid_entries_error('groups', groups, yaml_file)
            raise Exception(error)

        for group in groups:
            validate_yaml_group(group, yaml_file)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_import_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file with import"""
    _validate_type_dict(project, 'project', yaml_file)
    if not project:
        error = format_invalid_entries_error('project', project, yaml_file)
        raise Exception(error)

    if 'name' not in project:
        error = format_missing_entry_error('name', 'project', yaml_file)
        raise Exception(error)
    _validate_type_str(project['name'], 'name', yaml_file)
    del project['name']

    if not project:
        error = format_invalid_entries_error('project', project, yaml_file)
        raise Exception(error)

    if 'path' in project:
        _validate_type_str(project['path'], 'path', yaml_file)
        del project['path']

    validate_yaml_project_optional(project, yaml_file)

    if project:
        error = format_invalid_entries_error('project', project, yaml_file)
        raise Exception(error)


def validate_yaml_import_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file with import"""
    _validate_type_dict(group, 'group', yaml_file)
    if not group:
        error = format_invalid_entries_error('group', group, yaml_file)
        raise Exception(error)

    if 'name' not in group:
        error = format_missing_entry_error('name', 'group', yaml_file)
        raise Exception(error)
    _validate_type_str(group['name'], 'name', yaml_file)
    del group['name']

    if not group:
        error = format_invalid_entries_error('group', group, yaml_file)
        raise Exception(error)

    if 'projects' in group:
        validate_yaml_projects(group['projects'], yaml_file, is_import=True)
        del group['projects']

    if 'recursive' in group:
        _validate_type_bool(group['recursive'], 'recursive', yaml_file)
        del group['recursive']

    if 'ref' in group:
        _validate_type_str(group['ref'], 'ref', yaml_file)
        if not _valid_ref_type(group['ref']):
            error = format_invalid_ref_error(group['ref'], yaml_file)
            raise Exception(error)
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
        error = format_invalid_entries_error('group', group, yaml_file)
        raise Exception(error)


def validate_yaml_group(group, yaml_file):
    """Validate group in clowder loaded from yaml file"""
    _validate_type_dict(group, 'group', yaml_file)
    if not group:
        error = format_invalid_entries_error('group', group, yaml_file)
        raise Exception(error)

    if 'name' not in group:
        error = format_missing_entry_error('name', 'group', yaml_file)
        raise Exception(error)
    _validate_type_str(group['name'], 'name', yaml_file)
    del group['name']

    if 'projects' not in group:
        error = format_missing_entry_error('projects', 'group', yaml_file)
        raise Exception(error)
    validate_yaml_projects(group['projects'], yaml_file, is_import=False)
    del group['projects']

    if 'recursive' in group:
        _validate_type_bool(group['recursive'], 'recursive', yaml_file)
        del group['recursive']

    if 'ref' in group:
        _validate_type_str(group['ref'], 'ref', yaml_file)
        if not _valid_ref_type(group['ref']):
            error = format_invalid_ref_error(group['ref'], yaml_file)
            raise Exception(error)
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
        error = format_invalid_entries_error('group', group, yaml_file)
        raise Exception(error)


def validate_yaml_project(project, yaml_file):
    """Validate project in clowder loaded from yaml file"""
    _validate_type_dict(project, 'project', yaml_file)
    if not project:
        error = format_invalid_entries_error('project', project, yaml_file)
        raise Exception(error)

    if 'name' not in project:
        error = format_missing_entry_error('name', 'project', yaml_file)
        raise Exception(error)
    _validate_type_str(project['name'], 'name', yaml_file)
    del project['name']

    if 'path' not in project:
        error = format_missing_entry_error('path', 'project', yaml_file)
        raise Exception(error)
    _validate_type_str(project['path'], 'path', yaml_file)
    del project['path']

    validate_yaml_project_optional(project, yaml_file)

    if project:
        error = format_invalid_entries_error('project', project, yaml_file)
        raise Exception(error)


def validate_yaml_project_optional(project, yaml_file):
    """Validate optional args in project in clowder loaded from yaml file"""
    if 'remote' in project:
        _validate_type_str(project['remote'], 'remote', yaml_file)
        del project['remote']

    if 'recursive' in project:
        _validate_type_bool(project['recursive'], 'recursive', yaml_file)
        del project['recursive']

    if 'ref' in project:
        _validate_type_str(project['ref'], 'ref', yaml_file)
        if not _valid_ref_type(project['ref']):
            error = format_invalid_ref_error(project['ref'], yaml_file)
            raise Exception(error)
        del project['ref']

    if 'source' in project:
        _validate_type_str(project['source'], 'source', yaml_file)
        del project['source']

    if 'depth' in project:
        _validate_type_depth(project['depth'], yaml_file)
        del project['depth']

    if 'fork' in project:
        fork = project['fork']
        validate_yaml_fork(fork, yaml_file)
        del project['fork']


def validate_yaml_projects(projects, yaml_file, is_import):
    """Validate projects in clowder loaded from yaml file"""
    try:
        _validate_type_list(projects, 'projects', yaml_file)
        if not projects:
            error = format_invalid_entries_error('projects', projects, yaml_file)
            raise Exception(error)

        for project in projects:
            if is_import:
                validate_yaml_import_project(project, yaml_file)
            else:
                validate_yaml_project(project, yaml_file)

    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


def validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file"""
    try:
        _validate_type_list(sources, 'sources', yaml_file)
        if not sources:
            error = format_invalid_entries_error('sources', sources, yaml_file)
            raise Exception(error)

        for source in sources:
            _validate_type_dict(source, 'source', yaml_file)
            if not source:
                error = format_invalid_entries_error('source', source, yaml_file)
                raise Exception(error)

            if 'name' not in source:
                error = format_missing_entry_error('name', 'source', yaml_file)
                raise Exception(error)
            _validate_type_str(source['name'], 'name', yaml_file)
            del source['name']

            if 'url' not in source:
                error = format_missing_entry_error('url', 'source', yaml_file)
                raise Exception(error)
            _validate_type_str(source['url'], 'url', yaml_file)
            del source['url']

            if source:
                error = format_invalid_entries_error('source', source, yaml_file)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)


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


def _validate_type_bool(value, name, yaml_file):
    """Validate value is a bool"""
    if not isinstance(value, bool):
        error = format_not_bool_error(name, yaml_file)
        raise Exception(error)


def _validate_type_depth(value, yaml_file):
    """Validate depth value"""
    error = format_depth_error(value, yaml_file)
    if not isinstance(value, int):
        raise Exception(error)
    if int(value) < 0:
        raise Exception(error)


def _validate_type_dict(value, name, yaml_file):
    """Validate value is a dict"""
    if not isinstance(value, dict):
        error = format_not_dictionary_error(name, yaml_file)
        raise Exception(error)


def _validate_type_list(value, name, yaml_file):
    """Validate value is a list"""
    if not isinstance(value, list):
        error = format_not_list_error(name, yaml_file)
        raise Exception(error)


def _validate_type_str(value, name, yaml_file):
    """Validate value is a str"""
    if not isinstance(value, str):
        error = format_not_string_error(name, yaml_file)
        raise Exception(error)
