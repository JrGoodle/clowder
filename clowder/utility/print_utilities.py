"""Print utilities"""
import os
from termcolor import colored
from clowder.utility.git_utilities import (
    git_current_sha,
    git_current_branch,
    git_is_detached,
    git_is_dirty
)

def print_repo_status(repo_path, name):
    """Print repo status"""
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

    print(project_output + ' ' + current_ref_output)
