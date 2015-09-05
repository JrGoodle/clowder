"""Clowder utilities"""
import os
from git import Repo
from clowder.utility.git_utilities import (
    git_checkout_ref,
    git_clone_url_at_path,
    git_create_remote,
    git_fetch,
    git_is_detached,
    git_is_dirty,
    git_pull,
    git_ref_type,
    git_truncate_ref
)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

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
