"""Clowder yaml validation"""
import sys
from clowder.utility.print_utilities import (
    format_depth_error,
    format_missing_entry_error,
    format_not_array_error,
    format_unknown_entries_error,
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

def validate_yaml(parsed_yaml):
    """Validate clowder.yaml without no import"""
    try:
        if 'defaults' not in parsed_yaml:
            error = format_missing_entry_error('\'defaults\'', format_yaml_file('clowder.yaml'))
            raise Exception(error)
        defaults = parsed_yaml['defaults']
        validate_yaml_defaults(defaults)
        del parsed_yaml['defaults']

        if 'sources' not in parsed_yaml:
            error = format_missing_entry_error('\'sources\'', format_yaml_file('clowder.yaml'))
            raise Exception(error)
        sources = parsed_yaml['sources']
        validate_yaml_sources(sources)
        del parsed_yaml['sources']

        if 'groups' not in parsed_yaml:
            error = format_missing_entry_error('\'groups\'', format_yaml_file('clowder.yaml'))
            raise Exception(error)
        groups = parsed_yaml['groups']
        validate_yaml_groups(groups)
        del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            error = format_unknown_entries_error(format_yaml_file('clowder.yaml'), parsed_yaml)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_import(parsed_yaml):
    """Validate clowder.yaml with an import"""
    try:
        if 'import' not in parsed_yaml:
            error = format_missing_entry_error('\'import\'', format_yaml_file('clowder.yaml'))
            raise Exception(error)
        del parsed_yaml['import']

        if 'defaults' in parsed_yaml:
            defaults = parsed_yaml['defaults']
            if 'ref' in defaults:
                del defaults['ref']
            if 'remote' in defaults:
                del defaults['remote']
            if 'source' in defaults:
                del defaults['source']
            if 'depth' in defaults:
                error = format_depth_error(defaults['depth'])
                if not isinstance(defaults['depth'], int):
                    raise Exception(error)
                if int(defaults['depth']) < 0:
                    raise Exception(error)
                del defaults['depth']
            if len(defaults) > 0:
                error = format_unknown_entries_error('\'defaults\'', defaults)
                raise Exception(error)
            del parsed_yaml['defaults']

        if 'sources' in parsed_yaml:
            validate_yaml_sources(parsed_yaml['sources'])
            del parsed_yaml['sources']

        if 'groups' in parsed_yaml:
            validate_yaml_groups(parsed_yaml['groups'])
            del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            error = format_unknown_entries_error(format_yaml_file('clowder.yaml'), parsed_yaml)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_defaults(defaults):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        if 'ref' not in defaults:
            error = format_missing_entry_error('\'ref\'', '\'defaults\'')
            raise Exception(error)
        del defaults['ref']

        if 'remote' not in defaults:
            error = format_missing_entry_error('\'remote\'', '\'defaults\'')
            raise Exception(error)
        del defaults['remote']

        if 'source' not in defaults:
            error = format_missing_entry_error('\'source\'', '\'defaults\'')
            raise Exception(error)
        del defaults['source']

        if 'depth' in defaults:
            error = format_depth_error(defaults['depth'])
            if not isinstance(defaults['depth'], int):
                raise Exception(error)
            if int(defaults['depth']) < 0:
                raise Exception(error)
            del defaults['depth']

        if len(defaults) > 0:
            error = format_unknown_entries_error('\'defaults\'', defaults)
            raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_forks(forks):
    """Validate forks in clowder loaded from yaml file"""
    try:
        for fork in forks:
            if 'name' not in fork:
                error = format_missing_entry_error('\'name\'', '\'fork\'')
                raise Exception(error)
            del fork['name']
            if 'remote' not in fork:
                error = format_missing_entry_error('\'remote\'', '\'fork\'')
                raise Exception(error)
            del fork['remote']
            if len(fork) > 0:
                error = format_unknown_entries_error('\'fork\'', fork)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_groups(groups):
    """Validate groups in clowder loaded from yaml file"""
    try:
        if not isinstance(groups, list):
            error = format_not_array_error('\'groups\'')
            raise Exception(error)
        for group in groups:
            if 'name' not in group:
                error = format_missing_entry_error('\'name\'', '\'group\'')
                raise Exception(error)
            if 'projects' not in group:
                error = format_missing_entry_error('\'projects\'', '\'group\'')
                raise Exception(error)
            projects = group['projects']
            if not isinstance(projects, list):
                error = format_not_array_error('\'projects\'')
                raise Exception(error)
            validate_yaml_projects(projects)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_projects(projects):
    """Validate projects in clowder loaded from yaml file"""
    try:
        for project in projects:
            if 'name' not in project:
                error = format_missing_entry_error('\'name\'', '\'project\'')
                raise Exception(error)
            del project['name']

            if 'path' not in project:
                error = format_missing_entry_error('\'path\'', '\'project\'')
                raise Exception(error)
            del project['path']

            if 'remote' in project:
                del project['remote']
            if 'ref' in project:
                del project['ref']
            if 'source' in project:
                del project['source']
            if 'depth' in project:
                error = format_depth_error(project['depth'])
                if not isinstance(project['depth'], int):
                    raise Exception(error)
                if int(project['depth']) < 0:
                    raise Exception(error)
                del project['depth']
            if 'forks' in project:
                forks = project['forks']
                if not isinstance(forks, list):
                    error = format_not_array_error('\'forks\'')
                    raise Exception(error)
                validate_yaml_forks(forks)
                del project['forks']
            if len(project) > 0:
                error = format_unknown_entries_error('\'project\'', project)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)

def validate_yaml_sources(sources):
    """Validate sources in clowder loaded from yaml file"""
    try:
        if not isinstance(sources, list):
            error = format_not_array_error('\'sources\'')
            raise Exception(error)
        for source in sources:
            if 'name' not in source:
                error = format_missing_entry_error('\'name\'', '\'source\'')
                raise Exception(error)
            del source['name']

            if 'url' not in source:
                error = format_missing_entry_error('\'url\'', '\'source\'')
                raise Exception(error)
            del source['url']

            if len(source) > 0:
                error = format_unknown_entries_error('\'fork\'', source)
                raise Exception(error)
    except Exception as err:
        print_invalid_yaml_error()
        print_error(err)
        sys.exit(1)
