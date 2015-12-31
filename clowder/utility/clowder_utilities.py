"""Clowder utilities"""
import errno, os, subprocess, sys
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

def forall_run(command, directories):
    """Run command in all directories"""
    sorted_paths = sorted(set(directories))
    paths = [p for p in sorted_paths if os.path.isdir(p)]
    for path in paths:
        running_output = colored('Running command', attrs=['underline'])
        command_output = colored(command, attrs=['bold'])
        print(running_output + ': ' + command_output)
        directory_output = colored('Directory', attrs=['underline'])
        path_output = colored(path, 'cyan')
        print(directory_output + ': ' + path_output)
        subprocess.call(command.split(),
                        cwd=path)
        print('')
    # Exit early to prevent printing extra newline
    sys.exit()

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
        parsed_yaml['defaults']['ref']
        parsed_yaml['defaults']['remote']
        parsed_yaml['defaults']['source']

        for source in parsed_yaml['sources']:
            source['name']
            source['url']

        for group in parsed_yaml['groups']:
            group['name']
            for project in group['projects']:
                project['name']
                project['path']
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        sys.exit(1)
