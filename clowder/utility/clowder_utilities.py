"""Clowder utilities"""
import errno
import os
import sys
from termcolor import colored, cprint
from clowder.utility.git_utilities import (
    git_current_branch,
    git_current_sha,
    git_is_detached,
    git_is_dirty,
    git_new_local_commits,
    git_new_upstream_commits
)

def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)

def format_project_string(repo_path, name):
    """Return formatted project name"""
    if git_is_dirty(repo_path):
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(name + symbol, color)

def format_ref_string(repo_path):
    """Return formatted repo ref name"""
    local_commits = git_new_local_commits(repo_path)
    upstream_commits = git_new_upstream_commits(repo_path)
    no_local_commits = local_commits == 0 or local_commits == '0'
    no_upstream_commits = upstream_commits == 0 or upstream_commits == '0'
    if no_local_commits and no_upstream_commits:
        status = ''
    else:
        local_commits_output = colored('+' + str(local_commits), 'yellow')
        upstream_commits_output = colored('-' + str(upstream_commits), 'red')
        status = ' (' + local_commits_output + '/' + upstream_commits_output + ')'

    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta') + status

def print_exists(repo_path):
    """Print existence validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        cprint(' - Project is missing', 'red')

def print_validation(repo_path):
    """Print validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return
    if git_is_dirty(repo_path):
        print(' - Dirty repo. Please stash, commit, or discard your changes')

# http://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return not git_is_dirty(repo_path)

def validate_yaml(parsed_yaml):
    """Validate clowder loaded from yaml file"""
    validate_yaml_defaults(parsed_yaml)
    validate_yaml_sources(parsed_yaml)
    validate_yaml_groups(parsed_yaml)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104

def validate_yaml_defaults(parsed_yaml):
    """Validate defaults in clowder loaded from yaml file"""
    try:
        error = colored('Missing \'defaults\'', 'red')
        defaults = parsed_yaml['defaults']
        error = colored('Missing \'ref\' in \'defaults\'\n', 'red')
        defaults['ref']
        del defaults['ref']
        error = colored('Missing \'remote\' in \'defaults\'\n', 'red')
        defaults['remote']
        del defaults['remote']
        error = colored('Missing \'source\' in \'defaults\'\n', 'red')
        defaults['source']
        del defaults['source']
        if 'depth' in defaults:
            if int(defaults['depth']) < 0:
                error = colored('\'depth\' must be a positive integer\n', 'red')
                raise Exception('Negative depth value')
            del defaults['depth']
        if len(defaults) > 0:
            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                   for key, val in sorted(defaults.items()))
            error = colored('Uknown entry in \'defaults\'\n\n' +
                            dict_entries, 'red')
            raise Exception('Unknown default value')
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        print(error)
        sys.exit(1)

def validate_yaml_sources(parsed_yaml):
    """Validate sources in clowder loaded from yaml file"""
    try:
        error = colored('Missing \'sources\'\n', 'red')
        sources = parsed_yaml['sources']
        for source in sources:
            error = colored('Missing \'name\' in \'sources\'\n', 'red')
            source['name']
            del source['name']
            error = colored('Missing \'url\' in \'sources\'\n', 'red')
            source['url']
            del source['url']
            if len(source) > 0:
                dict_entries = ''.join('{}: {}\n'.format(key, val)
                                       for key, val in sorted(source.items()))
                error = colored('Uknown entry in \'fork\'\n\n' +
                                dict_entries, 'red')
                raise Exception('Unknown fork value')
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        print(error)
        sys.exit(1)

# Disable errors shown by pylint for too many nested blocks
# pylint: disable=R0101
def validate_yaml_groups(parsed_yaml):
    """Validate groups in clowder loaded from yaml file"""
    try:
        error = colored('Missing \'groups\'\n', 'red')
        groups = parsed_yaml['groups']
        for group in groups:
            error = colored('Missing \'name\' in \'group\'\n', 'red')
            group['name']
            error = colored('Missing \'projects\' in \'group\'\n', 'red')
            for project in group['projects']:
                error = colored('Missing \'name\' in \'project\'\n', 'red')
                project['name']
                del project['name']
                error = colored('Missing \'path\' in \'project\'\n', 'red')
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
                        error = colored('\'depth\' must be a positive integer\n', 'red')
                        raise Exception('Negative depth value')
                    del project['depth']
                if 'forks' in project:
                    for fork in project['forks']:
                        error = colored('Missing \'name\' in \'fork\'\n', 'red')
                        fork['name']
                        del fork['name']
                        error = colored('Missing \'remote\' in \'fork\'\n', 'red')
                        fork['remote']
                        del fork['remote']
                        if len(fork) > 0:
                            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                                   for key, val in sorted(fork.items()))
                            error = colored('Uknown entry in \'fork\'\n\n' +
                                            dict_entries, 'red')
                            raise Exception('Unknown fork value')
                    del project['forks']
                if len(project) > 0:
                    dict_entries = ''.join('{}: {}\n'.format(key, val)
                                           for key, val in sorted(project.items()))
                    error = colored('Uknown entry in \'project\'\n\n' +
                                    dict_entries, 'red')
                    raise Exception('Unknown project value')
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        print(error)
        sys.exit(1)
