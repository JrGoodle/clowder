# -*- coding: utf-8 -*-
"""Clowder git utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from clowder.error. clowder_error import ClowderError


def existing_git_repository(path: str) -> bool:
    """Check if a git repository exists

    :param str path: Repo path
    :return: True, if .git directory exists inside path
    :rtype: bool
    """

    return os.path.isdir(os.path.join(path, '.git'))


def existing_git_submodule(path: str) -> bool:
    """Check if a git submodule exists

    :param str path: Submodule path
    :return: True, if .git file exists inside path
    :rtype: bool
    """

    return os.path.isfile(os.path.join(path, '.git'))


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached(print_output=True):
            return
        return func(*args, **kwargs)

    return wrapper


def git_url(protocol: str, url: str, name: str) -> str:
    """Return git url

    :param str protocol: Git protocol ('ssh' or 'https')
    :param str url: Repo url
    :param str name: Repo name
    :return: Full git repo url for specified protocol
    :rtype: str
    :raise ClowderError:
    """

    if protocol == 'ssh':
        return 'git@' + url + ':' + name + ".git"

    if protocol == 'https':
        return 'https://' + url + '/' + name + ".git"

    raise ClowderError


def ref_type(ref: str) -> str:
    """Return branch, tag, sha, or unknown ref type

    :param str ref: Full pathspec
    :return: 'branch', 'tag', 'sha', or 'unknown'
    :rtype: str
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return 'branch'
    elif ref.startswith(git_tag):
        return 'tag'
    elif len(ref) == 40:
        return 'sha'
    return 'unknown'


def truncate_ref(ref: str) -> str:
    """Return bare branch, tag, or sha

    :param str ref: Full pathspec or short ref
    :return: Ref with 'refs/heads/' and 'refs/tags/' prefix removed
    :rtype: str
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        length = len(git_branch)
    elif ref.startswith(git_tag):
        length = len(git_tag)
    else:
        length = 0
    return ref[length:]
