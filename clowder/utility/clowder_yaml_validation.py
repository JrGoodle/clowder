"""Clowder yaml validation"""
import sys
from clowder.utility.clowder_utilities import parse_yaml
from clowder.utility.print_utilities import (
    format_depth_error,
    format_empty_yaml_error,
    format_missing_entry_error,
    format_not_dictionary_error,
    format_not_list_error,
    format_not_string_error,
    format_invalid_entries_error,
    format_yaml_file,
    print_error,
    print_invalid_yaml_error
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703
# Disable errors shown by pylint for too many branches
# pylint: disable=R0912
# Disable errors shown by pylint for too many statements
# pylint: disable=R0915

def validate_yaml(yaml_file):
    """Validate clowder.yaml with no import"""
    parsed_yaml = parse_yaml(yaml_file)
    try:
        if not isinstance(parsed_yaml, dict):
            error = format_not_dictionary_error(format_yaml_file('clowder.yaml'),
                                                yaml_file)
            raise Exception(error)
        if len(parsed_yaml) is 0:
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

        if len(parsed_yaml) > 0:
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
        if not isinstance(parsed_yaml, dict):
            error = format_not_dictionary_error(format_yaml_file('clowder.yaml'),
                                                yaml_file)
            raise Exception(error)

        if 'import' not in parsed_yaml:
            error = format_missing_entry_error('import',
                                               format_yaml_file('clowder.yaml'),
                                               yaml_file)
            raise Exception(error)
        if not isinstance(parsed_yaml['import'], str):
            error = format_not_string_error('import', yaml_file)
            raise Exception(error)
        del parsed_yaml['import']

        if len(parsed_yaml) is 0:
            error = format_empty_yaml_error(yaml_file)
            raise Exception(error)

        if 'defaults' in parsed_yaml:
            defaults = parsed_yaml['defaults']
            if not isinstance(defaults, dict):
                error = format_not_dict_error('defaults')
                raise Exception(error)
            if 'ref' in defaults:
                if not isinstance(defaults['ref'], str):
                    error = format_not_string_error('ref', yaml_file)
                    raise Exception(error)
                del defaults['ref']
            if 'remote' in defaults:
                if not isinstance(defaults['remote'], str):
                    error = format_not_string_error('remote', yaml_file)
                    raise Exception(error)
                del defaults['remote']
            if 'source' in defaults:
                if not isinstance(defaults['source'], str):
                    error = format_not_string_error('source', yaml_file)
                    raise Exception(error)
                del defaults['source']
            if 'depth' in defaults:
                error = format_depth_error(defaults['depth'], yaml_file)
                if not isinstance(defaults['depth'], int):
                    raise Exception(error)
                if int(defaults['depth']) < 0:
                    raise Exception(error)
                del defaults['depth']
            if len(defaults) > 0:
                error = format_invalid_entries_error('defaults', defaults, yaml_file)
                raise Exception(error)
            del parsed_yaml['defaults']

        if 'sources' in parsed_yaml:
            validate_yaml_sources(parsed_yaml['sources'], yaml_file)
            del parsed_yaml['sources']

        if 'groups' in parsed_yaml:
            validate_yaml_groups(parsed_yaml['groups'], yaml_file)
            del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            error = format_invalid_entries_error(format_yaml_file('clowder.yaml'),
                                                 parsed_yaml, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_defaults(defaults, yaml_file):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        if not isinstance(defaults, dict):
            error = format_not_dictionary_error('defaults', yaml_file)
            raise Exception(error)
        if len(defaults) is 0:
            error = format_invalid_entries_error('defaults', defaults, yaml_file)
            raise Exception(error)

        if 'ref' not in defaults:
            error = format_missing_entry_error('ref', 'defaults', yaml_file)
            raise Exception(error)
        if not isinstance(defaults['ref'], str):
            error = format_not_string_error('ref', yaml_file)
            raise Exception(error)
        del defaults['ref']

        if 'remote' not in defaults:
            error = format_missing_entry_error('remote', 'defaults', yaml_file)
            raise Exception(error)
        if not isinstance(defaults['remote'], str):
            error = format_not_string_error('remote', yaml_file)
            raise Exception(error)
        del defaults['remote']

        if 'source' not in defaults:
            error = format_missing_entry_error('source', 'defaults', yaml_file)
            raise Exception(error)
        if not isinstance(defaults['source'], str):
            error = format_not_string_error('source', yaml_file)
            raise Exception(error)
        del defaults['source']

        if 'depth' in defaults:
            error = format_depth_error(defaults['depth'], yaml_file)
            if not isinstance(defaults['depth'], int):
                raise Exception(error)
            if int(defaults['depth']) < 0:
                raise Exception(error)
            del defaults['depth']

        if len(defaults) > 0:
            error = format_invalid_entries_error('defaults', defaults, yaml_file)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_forks(forks, yaml_file):
    """Validate forks in clowder loaded from yaml file"""
    try:
        if not isinstance(forks, list):
            error = format_not_list_error('forks', yaml_file)
            raise Exception(error)
        if len(forks) is 0:
            error = format_invalid_entries_error('forks', forks, yaml_file)
            raise Exception(error)

        for fork in forks:
            if not isinstance(fork, dict):
                error = format_not_dictionary_error('fork', yaml_file)
                raise Exception(error)
            if len(fork) is 0:
                error = format_invalid_entries_error('fork', fork, yaml_file)
                raise Exception(error)

            if 'name' not in fork:
                error = format_missing_entry_error('name', 'fork', yaml_file)
                raise Exception(error)
            if not isinstance(fork['name'], str):
                error = format_not_string_error('name', yaml_file)
                raise Exception(error)
            del fork['name']

            if 'remote' not in fork:
                error = format_missing_entry_error('remote', 'fork', yaml_file)
                raise Exception(error)
            if not isinstance(fork['remote'], str):
                error = format_not_string_error('remote', yaml_file)
                raise Exception(error)
            del fork['remote']

            if len(fork) > 0:
                error = format_invalid_entries_error('fork', fork, yaml_file)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_groups(groups, yaml_file):
    """Validate groups in clowder loaded from yaml file"""
    try:
        if not isinstance(groups, list):
            error = format_not_list_error('groups', yaml_file)
            raise Exception(error)
        if len(groups) is 0:
            error = format_invalid_entries_error('groups', groups, yaml_file)
            raise Exception(error)

        for group in groups:
            if not isinstance(group, dict):
                error = format_not_dictionary_error('group', yaml_file)
                raise Exception(error)
            if len(group) is 0:
                error = format_invalid_entries_error('group', group, yaml_file)
                raise Exception(error)

            if 'name' not in group:
                error = format_missing_entry_error('name', 'group', yaml_file)
                raise Exception(error)
            if not isinstance(group['name'], str):
                error = format_not_string_error('name', yaml_file)
                raise Exception(error)
            del group['name']

            if 'projects' not in group:
                error = format_missing_entry_error('projects', 'group', yaml_file)
                raise Exception(error)
            validate_yaml_projects(group['projects'], yaml_file)
            del group['projects']

            if len(group) > 0:
                error = format_invalid_entries_error('group', fork, yaml_file)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_projects(projects, yaml_file):
    """Validate projects in clowder loaded from yaml file"""
    try:
        if not isinstance(projects, list):
            error = format_not_list_error('projects', yaml_file)
            raise Exception(error)
        if len(projects) is 0:
            error = format_invalid_entries_error('projects', projects, yaml_file)
            raise Exception(error)

        for project in projects:
            if not isinstance(project, dict):
                error = format_not_dictionary_error('project', yaml_file)
                raise Exception(error)
            if len(project) is 0:
                error = format_invalid_entries_error('project', project, yaml_file)
                raise Exception(error)

            if 'name' not in project:
                error = format_missing_entry_error('name', 'project', yaml_file)
                raise Exception(error)
            if not isinstance(project['name'], str):
                error = format_not_string_error('name', yaml_file)
                raise Exception(error)
            del project['name']

            if 'path' not in project:
                error = format_missing_entry_error('path', 'project', yaml_file)
                raise Exception(error)
            if not isinstance(project['path'], str):
                error = format_not_string_error('path', yaml_file)
                raise Exception(error)
            del project['path']

            if 'remote' in project:
                if not isinstance(project['remote'], str):
                    error = format_not_string_error('remote', yaml_file)
                    raise Exception(error)
                del project['remote']

            if 'ref' in project:
                if not isinstance(project['ref'], str):
                    error = format_not_string_error('ref', yaml_file)
                    raise Exception(error)
                del project['ref']

            if 'source' in project:
                if not isinstance(project['source'], str):
                    error = format_not_string_error('source', yaml_file)
                    raise Exception(error)
                del project['source']

            if 'depth' in project:
                error = format_depth_error(project['depth'], yaml_file)
                if not isinstance(project['depth'], int):
                    raise Exception(error)
                if int(project['depth']) < 0:
                    raise Exception(error)
                del project['depth']

            if 'forks' in project:
                forks = project['forks']
                validate_yaml_forks(forks, yaml_file)
                del project['forks']

            if len(project) > 0:
                error = format_invalid_entries_error('project', project, yaml_file)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_sources(sources, yaml_file):
    """Validate sources in clowder loaded from yaml file"""
    try:
        if not isinstance(sources, list):
            error = format_not_list_error('sources', yaml_file)
            raise Exception(error)
        if len(sources) is 0:
            error = format_invalid_entries_error('sources', sources, yaml_file)
            raise Exception(error)

        for source in sources:
            if not isinstance(source, dict):
                error = format_not_dictionary_error('source', yaml_file)
                raise Exception(error)
            if len(source) is 0:
                error = format_invalid_entries_error('source', source, yaml_file)
                raise Exception(error)

            if 'name' not in source:
                error = format_missing_entry_error('name', 'source', yaml_file)
                raise Exception(error)
            if not isinstance(source['name'], str):
                error = format_not_string_error('name', yaml_file)
                raise Exception(error)
            del source['name']

            if 'url' not in source:
                error = format_missing_entry_error('url', 'source', yaml_file)
                raise Exception(error)
            if not isinstance(source['url'], str):
                error = format_not_string_error('url', yaml_file)
                raise Exception(error)
            del source['url']

            if len(source) > 0:
                error = format_invalid_entries_error('source', source, yaml_file)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)
