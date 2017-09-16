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
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703

def validate_yaml(parsed_yaml):
    """Validate clowder.yaml without no import"""
    try:
        error = format_missing_entry_error('\'defaults\'', format_yaml_file('clowder.yaml'))
        defaults = parsed_yaml['defaults']
        validate_yaml_defaults(defaults)
        del parsed_yaml['defaults']

        error = format_missing_entry_error('\'sources\'', format_yaml_file('clowder.yaml'))
        sources = parsed_yaml['sources']
        validate_yaml_sources(sources)
        del parsed_yaml['sources']

        error = format_missing_entry_error('\'groups\'', format_yaml_file('clowder.yaml'))
        groups = parsed_yaml['groups']
        validate_yaml_groups(groups)
        del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            error = format_unknown_entries_error(format_yaml_file('clowder.yaml'), parsed_yaml)
            raise Exception('Unknown clowder.yaml value')
    except Exception as err:
        print_invalid_yaml_error()
        print(error)
        print_error(err)
        sys.exit(1)

def validate_yaml_import(parsed_yaml):
    """Validate clowder.yaml with an import"""
    try:
        if 'import' not in parsed_yaml:
            error = format_missing_entry_error('\'import\'', format_yaml_file('clowder.yaml'))
            raise Exception('Missing import in clowder.yaml')
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
                if int(defaults['depth']) < 0:
                    raise Exception('Invalid depth value')
                del defaults['depth']
            if len(defaults) > 0:
                error = format_unknown_entries_error('\'defaults\'', defaults)
                raise Exception('Unknown default value')
            del parsed_yaml['defaults']

        if 'sources' in parsed_yaml:
            validate_yaml_sources(parsed_yaml['sources'])
            del parsed_yaml['sources']

        if 'groups' in parsed_yaml:
            validate_yaml_groups(parsed_yaml['groups'])
            del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            error = format_unknown_entries_error(format_yaml_file('clowder.yaml'), parsed_yaml)
            raise Exception('Unknown clowder.yaml value')
    except Exception as err:
        print_invalid_yaml_error()
        print(error)
        print_error(err)
        sys.exit(1)

def validate_yaml_defaults(defaults):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        error = format_missing_entry_error('\'ref\'', '\'defaults\'')
        defaults['ref']
        del defaults['ref']

        error = format_missing_entry_error('\'remote\'', '\'defaults\'')
        defaults['remote']
        del defaults['remote']

        error = format_missing_entry_error('\'source\'', '\'defaults\'')
        defaults['source']
        del defaults['source']

        if 'depth' in defaults:
            error = format_depth_error(defaults['depth'])
            if int(defaults['depth']) < 0:
                raise Exception('Invalid depth value')
            del defaults['depth']

        if len(defaults) > 0:
            error = format_unknown_entries_error('\'defaults\'', defaults)
            raise Exception('Unknown default value')
    except Exception as err:
        print_invalid_yaml_error()
        print(error)
        print_error(err)
        sys.exit(1)

def validate_yaml_sources(sources):
    """Validate sources in clowder loaded from yaml file"""
    try:
        error = format_not_array_error('\'sources\'')
        for source in sources:
            error = format_missing_entry_error('\'name\'', '\'sources\'')
            source['name']
            del source['name']

            error = format_missing_entry_error('\'url\'', '\'sources\'')
            source['url']
            del source['url']

            if len(source) > 0:
                error = format_unknown_entries_error('\'fork\'', source)
                raise Exception('Unknown fork value')
    except Exception as err:
        print_invalid_yaml_error()
        print(error)
        print_error(err)
        sys.exit(1)

# Disable errors shown by pylint for too many nested blocks
# pylint: disable=R0101

def validate_yaml_groups(groups):
    """Validate groups in clowder loaded from yaml file"""
    try:
        error = format_not_array_error('\'groups\'')
        for group in groups:
            error = format_missing_entry_error('\'name\'', '\'group\'')
            group['name']
            error = format_missing_entry_error('\'projects\'', '\'group\'')
            projects = group['projects']
            error = format_not_array_error('\'projects\'')
            for project in projects:
                error = format_missing_entry_error('\'name\'', '\'project\'')
                project['name']
                del project['name']

                error = format_missing_entry_error('\'path\'', '\'project\'')
                project['path']
                del project['path']

                if 'remote' in project:
                    del project['remote']
                if 'ref' in project:
                    del project['ref']
                if 'source' in project:
                    del project['source']
                if 'depth' in project:
                    error = format_depth_error(project['depth'])
                    if int(project['depth']) < 0:
                        raise Exception('Invalid depth value')
                    del project['depth']
                if 'forks' in project:
                    for fork in project['forks']:
                        error = format_missing_entry_error('\'name\'', '\'fork\'')
                        fork['name']
                        del fork['name']
                        error = format_missing_entry_error('\'remote\'', '\'fork\'')
                        fork['remote']
                        del fork['remote']
                        if len(fork) > 0:
                            error = format_unknown_entries_error('\'fork\'', fork)
                            raise Exception('Unknown fork value')
                    del project['forks']

                if len(project) > 0:
                    error = format_unknown_entries_error('\'project\'', project)
                    raise Exception('Unknown project value')
    except Exception as err:
        print_invalid_yaml_error()
        print(error)
        print_error(err)
        sys.exit(1)
