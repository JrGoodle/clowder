"""Clowder repo management"""

from __future__ import print_function

import sys

from git import GitError
from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.git.repo import GitRepo


DEFAULT_REF = 'refs/heads/master'
DEFAULT_REMOTE = 'origin'


def add(path, files):
    """Add files in clowder repo to git index"""
    clowder = GitRepo(path, DEFAULT_REMOTE, DEFAULT_REF)
    try:
        print(' - Add files to git index')
        print(clowder.repo.git.add(files))
    except GitError as err:
        cprint(' - Failed to add files to git index', 'red')
        print(fmt.error(err))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    else:
        GitRepo.status_verbose(path)


def commit(path, message):
    """Commit current changes in clowder repo"""
    clowder = GitRepo(path, DEFAULT_REMOTE, DEFAULT_REF)
    try:
        print(' - Commit current changes')
        print(clowder.repo.git.commit(message=message))
    except GitError as err:
        cprint(' - Failed to commit current changes', 'red')
        print(fmt.error(err))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def pull(path):
    """Pull clowder repo upstream changes"""
    clowder = GitRepo(path, DEFAULT_REMOTE, DEFAULT_REF)
    if clowder.repo.head.is_detached:
        print(' - HEAD is detached')
        return
    try:
        print(' - Pull latest changes')
        print(clowder.repo.git.pull())
    except GitError as err:
        cprint(' - Failed to pull latest changes', 'red')
        print(fmt.error(err))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def push(path):
    """Push clowder repo changes"""
    clowder = GitRepo(path, DEFAULT_REMOTE, DEFAULT_REF)
    if clowder.repo.head.is_detached:
        print(' - HEAD is detached')
        return
    try:
        print(' - Push local changes')
        print(clowder.repo.git.push())
    except GitError as err:
        cprint(' - Failed to push local changes', 'red')
        print(fmt.error(err))
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
