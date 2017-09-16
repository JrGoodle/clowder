"""Clowder yaml validation"""
from termcolor import colored

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104

def validate_yaml(parsed_yaml):
    """Validate clowder.yaml without no import"""
    try:
        error = colored(' - Missing \'defaults\'', 'red')
        defaults = parsed_yaml['defaults']
        validate_yaml_defaults(defaults)
        del parsed_yaml['defaults']

        error = colored(' - Missing \'sources\'\n', 'red')
        sources = parsed_yaml['sources']
        validate_yaml_sources(sources)
        del parsed_yaml['sources']

        error = colored(' - Missing \'groups\'\n', 'red')
        groups = parsed_yaml['groups']
        validate_yaml_groups(groups)
        del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                   for key, val in sorted(parsed_yaml.items()))
            error = colored(' - Unknown entry in \'clowder.yaml\'\n\n' +
                            dict_entries, 'red')
            raise Exception('Unknown clowder.yaml value')
    except Exception as err:
        print()
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print(error)
        message = colored(' - Error: ', 'red')
        print(message + str(err))
        raise

def validate_yaml_import(parsed_yaml):
    """Validate clowder.yaml with an import"""
    try:
        if 'import' not in parsed_yaml:
            error = colored(' - Missing \'import\' in clowder.yaml\n', 'red')
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
                if int(defaults['depth']) < 0:
                    error = colored(' - \'depth\' must be a positive integer\n', 'red')
                    raise Exception('Negative depth value')
                del defaults['depth']
            if len(defaults) > 0:
                dict_entries = ''.join('{}: {}\n'.format(key, val)
                                       for key, val in sorted(defaults.items()))
                error = colored(' - Unknown entry in \'defaults\'\n\n' +
                                dict_entries, 'red')
                raise Exception('Unknown default value')
            del parsed_yaml['defaults']

        if 'sources' in parsed_yaml:
            validate_yaml_sources(parsed_yaml['sources'])
            del parsed_yaml['sources']

        if 'groups' in parsed_yaml:
            validate_yaml_groups(parsed_yaml['groups'])
            del parsed_yaml['groups']

        if len(parsed_yaml) > 0:
            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                   for key, val in sorted(parsed_yaml.items()))
            error = colored(' - Unknown entry in clowder.yaml\n\n' +
                            dict_entries, 'red')
            raise Exception('Unknown clowder.yaml value')
    except Exception as err:
        print()
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print(error)
        message = colored(' - Error: ', 'red')
        print(message + str(err))
        raise

def validate_yaml_defaults(defaults):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        error = colored(' - Missing \'ref\' in \'defaults\'\n', 'red')
        defaults['ref']
        del defaults['ref']

        error = colored(' - Missing \'remote\' in \'defaults\'\n', 'red')
        defaults['remote']
        del defaults['remote']

        error = colored(' - Missing \'source\' in \'defaults\'\n', 'red')
        defaults['source']
        del defaults['source']

        if 'depth' in defaults:
            if int(defaults['depth']) < 0:
                error = colored(' - \'depth\' must be a positive integer\n', 'red')
                raise Exception('Negative depth value')
            del defaults['depth']

        if len(defaults) > 0:
            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                   for key, val in sorted(defaults.items()))
            error = colored(' - Unknown entry in \'defaults\'\n\n' +
                            dict_entries, 'red')
            raise Exception('Unknown default value')
    except Exception as err:
        print()
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print(error)
        message = colored(' - Error: ', 'red')
        print(message + str(err))
        raise

def validate_yaml_sources(sources):
    """Validate sources in clowder loaded from yaml file"""
    try:
        error = colored(' - \'sources\' doesn\'t contain array\n', 'red')
        for source in sources:
            error = colored(' - Missing \'name\' in \'sources\'\n', 'red')
            source['name']
            del source['name']

            error = colored(' - Missing \'url\' in \'sources\'\n', 'red')
            source['url']
            del source['url']

            if len(source) > 0:
                dict_entries = ''.join('{}: {}\n'.format(key, val)
                                       for key, val in sorted(source.items()))
                error = colored(' - Unknown entry in \'fork\'\n\n' +
                                dict_entries, 'red')
                raise Exception('Unknown fork value')
    except Exception as err:
        print()
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print(error)
        message = colored(' - Error: ', 'red')
        print(message + str(err))
        raise

# Disable errors shown by pylint for too many nested blocks
# pylint: disable=R0101

def validate_yaml_groups(groups):
    """Validate groups in clowder loaded from yaml file"""
    try:
        error = colored(' - \'groups\' doesn\'t contain array\n', 'red')
        for group in groups:
            error = colored(' - Missing \'name\' in \'group\'\n', 'red')
            group['name']
            error = colored(' - Missing \'projects\' in \'group\'\n', 'red')
            projects = group['projects']
            error = colored(' - \'projects\' doesn\'t contain array\n', 'red')
            for project in projects:
                error = colored(' - Missing \'name\' in \'project\'\n', 'red')
                project['name']
                del project['name']

                error = colored(' - Missing \'path\' in \'project\'\n', 'red')
                project['path']
                del project['path']

                if 'remote' in project:
                    del project['remote']
                if 'ref' in project:
                    del project['ref']
                if 'source' in project:
                    del project['source']
                if 'depth' in project:
                    if int(project['depth']) < 0:
                        error = colored(' - \'depth\' must be a positive integer\n', 'red')
                        raise Exception('Negative depth value')
                    del project['depth']
                if 'forks' in project:
                    for fork in project['forks']:
                        error = colored(' - Missing \'name\' in \'fork\'\n', 'red')
                        fork['name']
                        del fork['name']
                        error = colored(' - Missing \'remote\' in \'fork\'\n', 'red')
                        fork['remote']
                        del fork['remote']
                        if len(fork) > 0:
                            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                                   for key, val in sorted(fork.items()))
                            error = colored(' - Unknown entry in \'fork\'\n\n' +
                                            dict_entries, 'red')
                            raise Exception('Unknown fork value')
                    del project['forks']

                if len(project) > 0:
                    dict_entries = ''.join('{}: {}\n'.format(key, val)
                                           for key, val in sorted(project.items()))
                    error = colored(' - Unknown entry in \'project\'\n\n' +
                                    dict_entries, 'red')
                    raise Exception('Unknown project value')
    except Exception as err:
        print()
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print(error)
        message = colored(' - Error: ', 'red')
        print(message + str(err))
        raise
