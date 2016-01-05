"""Clowder utilities"""
import errno, os, sys
from termcolor import colored
from clowder.utility.git_utilities import (
    git_current_branch,
    git_current_sha,
    git_is_detached,
    git_is_dirty
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
    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta')

def print_exists(repo_path):
    """Print existence validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(' - Project is missing')

def print_validation(repo_path):
    """Print validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return
    if git_is_dirty(repo_path):
        print(' - Dirty repo. Please stash, commit, or discard your changes')

def validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return not git_is_dirty(repo_path)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104
def validate_yaml(parsed_yaml):
    """Load clowder from yaml file"""
    try:
        defaults = parsed_yaml['defaults']
        defaults['ref']
        del defaults['ref']
        defaults['remote']
        del defaults['remote']
        defaults['source']
        del defaults['source']
        if 'depth' in defaults:
            del defaults['depth']
        if len(defaults) > 0:
            raise Exception('Unknown default values')

        for source in parsed_yaml['sources']:
            source['name']
            source['url']

        for group in parsed_yaml['groups']:
            group['name']
            for project in group['projects']:
                project['name']
                del project['name']
                project['path']
                del project['path']
                if 'remote' in project:
                    del project['remote']
                if 'ref' in project:
                    del project['ref']
                if 'source' in project:
                    del project['source']
                if 'depth' in project:
                    del project['depth']
                if 'forks' in project:
                    for fork in project['forks']:
                        fork['name']
                        fork['remote']
                    del project['forks']
                if len(project) > 0:
                    raise Exception('Unknown project values')
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        sys.exit(1)
