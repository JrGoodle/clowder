# -*- coding: utf-8 -*-
"""Clowder git utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path

from git import Repo, GitError

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType


def check_ref_format(ref: str) -> bool:
    """Check if git ref is correctly formatted

    :param str ref: Git ref
    :return: True, if git ref is a valid format
    :rtype: bool
    """
    try:
        Repo().git.check_ref_format('--normalize', ref)
    except GitError as err:
        print(err)
        return False
    else:
        return True


def existing_git_repository(path: Path) -> bool:
    """Check if a git repository exists

    :param Path path: Repo path
    :return: True, if .git directory exists inside path
    :rtype: bool
    """

    return path.is_dir() and Path(path / '.git').is_dir()


def existing_git_submodule(path: Path) -> bool:
    """Check if a git submodule exists

    :param Path path: Submodule path
    :return: True, if .git file exists inside path
    :rtype: bool
    """

    return Path(path / '.git').is_file()


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached(print_output=True):
            return
        return func(*args, **kwargs)

    return wrapper


def format_git_branch(branch: str) -> str:
    """Returns properly formatted git branch

    :param str branch: Git branch name
    :return: Branch prefixed with 'refs/heads/'
    :rtype: str
    """

    prefix = "refs/heads/"
    return branch if branch.startswith(prefix) else f"{prefix}{branch}"


def format_git_tag(tag: str) -> str:
    """Returns properly formatted git tag

    :param str tag: Git tag name
    :return: Tag prefixed with 'refs/heads/'
    :rtype: str
    """

    prefix = "refs/tags/"
    return tag if tag.startswith(prefix) else f"{prefix}{tag}"


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
        return f"git@{url}:{name}.git"

    if protocol == 'https':
        return f"https://{url}/{name}.git"

    raise ClowderError(ClowderErrorType.INVALID_GIT_URL, f"{fmt.ERROR} Invalid git protocol")


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
