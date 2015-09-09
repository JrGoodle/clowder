"""Clowder utilities"""
import os, subprocess, sys
from termcolor import colored, cprint
from clowder.utility.git_utilities import (
    git_checkout_ref,
    git_clone_url_at_path,
    git_create_remote,
    git_current_branch,
    git_current_sha,
    git_fetch,
    git_is_detached,
    git_is_dirty,
    git_pull,
    git_pull_remote_branch,
    git_ref_type,
    git_truncate_ref
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

def format_ref_string(repo_path):
    """Return formatted repo ref name"""
    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta')

def herd(repo_path, ref, remote, url):
    """Sync git repo with default branch"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        git_clone_url_at_path(url, repo_path, ref, remote)
    else:
        ref_type = git_ref_type(ref)
        if ref_type is 'branch':
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_ref(repo_path, ref, remote)
            branch = git_truncate_ref(ref)
            git_pull_remote_branch(repo_path, remote, branch)
        elif ref_type is 'tag' or ref_type is 'sha':
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_ref(repo_path, ref, remote)
        else:
            print('Unknown ref ' + ref)

def print_exists(repo_path):
    """Print existence validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(' - Project is missing')

def print_exiting():
    """Print Exiting and exit with error code"""
    print('')
    cprint('Exiting...', 'red')
    print('')
    sys.exit(1)

def print_validation(repo_path):
    """Print validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return
    if git_is_dirty(repo_path):
        print(' - Dirty repo. Please stash, commit, or discard your changes')

def sync(repo_path):
    """Sync clowder repo with current branch"""
    if not git_is_detached(repo_path):
        print(' - Pulling latest changes')
        git_pull(repo_path)

def validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return not git_is_dirty(repo_path)

def _forall_run(command, directories):
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

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104
def _validate_yaml(parsed_yaml):
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
        print_exiting()
