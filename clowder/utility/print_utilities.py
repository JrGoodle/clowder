"""Print utilities"""
import os
import emoji
from termcolor import colored, cprint
from clowder.utility.git_utilities import (
    git_current_sha,
    git_current_branch,
    git_is_detached,
    git_is_dirty
)

def get_cat_face():
    """Return a cat emoji"""
    return emoji.emojize(':cat:', use_aliases=True)

def get_cat():
    """Return a cat emoji"""
    return emoji.emojize(':cat2:', use_aliases=True)

def format_clowder_string(repo_path, name):
    """Return formatted string for clowder repo"""
    project_output = format_project_string(repo_path, name)
    current_ref_output = format_ref_string(repo_path)
    return project_output + ' ' + current_ref_output

def format_repo_string(repo_path, path, name):
    """Return formatted string for project"""
    project_output = format_project_string(repo_path, name)
    current_ref_output = format_ref_string(repo_path)
    path_output = colored(path, 'cyan')
    return project_output + ' ' + current_ref_output + ' ' + path_output

def format_project_string(repo_path, name):
    """Return formatted project name"""
    if git_is_dirty(repo_path):
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(symbol + name, color)

def format_ref_string(repo_path):
    """Return formatted repo ref name"""
    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta')

def print_clowder_not_found_message():
    """Print error message when clowder not found"""
    cprint('No clowder found in the current directory, exiting...\n', 'red')

def print_clowder_repo_status(root_directory):
    """Print clowder repo status"""
    repo_path = os.path.join(root_directory, 'clowder')
    git_path = os.path.join(repo_path, '.git')
    if not os.path.isdir(git_path):
        cprint('clowder', 'green')
        return
    output = format_clowder_string(repo_path, 'clowder')
    print(get_cat_face() + ' ' + output)

def print_group(name):
    """Print formatted group name"""
    name_output = colored(name, attrs=['bold', 'underline'])
    # print(get_cat_face() + '  ' + name_output)
    print(name_output)

def print_project_status(root_directory, path, name):
    """Print repo status"""
    repo_path = os.path.join(root_directory, path)
    git_path = os.path.join(repo_path, '.git')
    if not os.path.isdir(git_path):
        cprint(name, 'green')
        return
    print(format_repo_string(repo_path, path, name))
