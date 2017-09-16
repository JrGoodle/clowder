"""String formatting and printing utilities for git"""
from termcolor import colored, cprint
from clowder.utility.git_utilities import (
    git_current_branch,
    git_existing_repository,
    git_is_detached,
    git_is_dirty,
    git_new_local_commits,
    git_new_upstream_commits,
    git_sha_short
)

def format_project_string(repo_path, name):
    """Return formatted project name"""
    if git_is_dirty(repo_path):
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(name + symbol, color)

def format_project_ref_string(repo_path):
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
        current_ref = git_sha_short(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta') + status

def print_exists(repo_path):
    """Print existence validation messages"""
    if not git_existing_repository(repo_path):
        cprint(' - Project is missing', 'red')

def print_validation(repo_path):
    """Print validation messages"""
    if not git_existing_repository(repo_path):
        return
    if git_is_dirty(repo_path):
        print(' - Dirty repo. Please stash, commit, or discard your changes')
