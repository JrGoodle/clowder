"""Print utilities"""
import os
import emoji
from termcolor import colored
from clowder.utility.git_utilities import (
    git_current_sha,
    git_current_branch,
    git_is_detached,
    git_is_dirty
)

def print_project_status(root_directory, path, name):
    """Print repo status"""
    repo_path = os.path.join(root_directory, path)
    git_path = os.path.join(repo_path, '.git')
    if not os.path.isdir(git_path):
        return

    if git_is_dirty(repo_path):
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    project_output = colored(symbol + name, color)

    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        current_ref_output = colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        current_ref_output = colored('(' + current_branch + ')', 'magenta')

    path_output = colored(path, 'cyan')

    print(project_output)
    print(current_ref_output + ' ' + path_output)

def print_group(name):
    name_output = colored(name, attrs=['bold'])
    print(get_cat() + '  ' + name_output)

def get_cat():
    """Return a cat emoji"""
    return emoji.emojize(':cat:', use_aliases=True)
