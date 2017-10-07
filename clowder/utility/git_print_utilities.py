"""String formatting and printing utilities for git"""
import os
import sys
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import (
    execute_command,
    existing_git_repository,
)
from clowder.utility.git_utilities import Git
from clowder.utility.print_utilities import (
    format_command,
    print_command_failed_error
)

def format_project_string(repo_path, name):
    """Return formatted project name"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return colored(name, 'green')
    repo = Git(repo_path)
    if not repo.validate_repo():
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(name + symbol, color)

def format_project_ref_string(repo_path):
    """Return formatted repo ref name"""
    repo = Git(repo_path)
    local_commits = repo.new_commits()
    upstream_commits = repo.new_commits(upstream=True)
    no_local_commits = local_commits == 0 or local_commits == '0'
    no_upstream_commits = upstream_commits == 0 or upstream_commits == '0'
    if no_local_commits and no_upstream_commits:
        status = ''
    else:
        local_commits_output = colored('+' + str(local_commits), 'yellow')
        upstream_commits_output = colored('-' + str(upstream_commits), 'red')
        status = '[' + local_commits_output + '/' + upstream_commits_output + ']'

    if repo.is_detached():
        current_ref = repo.sha(short=True)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = repo.current_branch()
        return colored('(' + current_branch + ')', 'magenta') + status

def print_exists(repo_path):
    """Print existence validation messages"""
    if not existing_git_repository(repo_path):
        cprint(' - Project is missing', 'red')

def print_git_status(repo_path):
    """Print git status"""
    command = ['git', 'status', '-vv']
    print(format_command(command))
    return_code = execute_command(command, repo_path)
    if return_code != 0:
        cprint(' - Failed to print status', 'red')
        print_command_failed_error(command)
        sys.exit(return_code)

def print_validation(repo_path):
    """Print validation messages"""
    repo = Git(repo_path)
    if not existing_git_repository(repo_path):
        return
    if not repo.validate_repo():
        print(' - Dirty repo. Please stash, commit, or discard your changes')
        print_git_status(repo_path)
