"""Clowder utilities"""
import emoji, os, sys
from git import Repo
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
    git_ref_type,
    git_truncate_ref
)

def cat_face():
    """Return a cat emoji"""
    return emoji.emojize(':cat:', use_aliases=True)

def cat():
    """Return a cat emoji"""
    return emoji.emojize(':cat2:', use_aliases=True)

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

def groom(repo_path):
    """Discard current changes in repository"""
    repo = Repo(repo_path)
    if repo.is_dirty():
        print(' - Discarding current changes')
        repo.head.reset(index=True, working_tree=True)
    else:
        print(' - No changes to discard')

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
            git_pull(repo_path, remote, branch)
        elif ref_type is 'tag' or ref_type is 'sha':
            git_create_remote(repo_path, remote, url)
            git_fetch(repo_path)
            git_checkout_ref(repo_path, ref, remote)
        else:
            print('Unknown ref ' + ref)

def print_clowder_repo_status(root_directory):
    """Print clowder repo status"""
    repo_path = os.path.join(root_directory, 'clowder')
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        output = colored('clowder', 'green')
        print(cat_face() + ' ' + output)
        return
    project_output = format_project_string(repo_path, 'clowder')
    current_ref_output = format_ref_string(repo_path)
    print(cat_face() + ' ' + project_output + ' ' + current_ref_output)

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
    git_fetch(repo_path)
    repo = Repo(repo_path)
    if not git_is_detached(repo_path):
        print(' - Pulling latest changes')
        print(repo.git.pull())

def validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return not git_is_dirty(repo_path)
