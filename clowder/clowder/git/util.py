# -*- coding: utf-8 -*-
"""Clowder git utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from termcolor import colored

from clowder.error. clowder_error import ClowderError


def existing_git_repository(path):
    """Check if a git repository exists

    :param str path: Repo path
    :return: True, if .git directory exists inside path
    :rtype: bool
    """

    return os.path.isdir(os.path.join(path, '.git'))


def existing_git_submodule(path):
    """Check if a git submodule exists

    :param str path: Submodule path
    :return: True, if .git file exists inside path
    :rtype: bool
    """

    return os.path.isfile(os.path.join(path, '.git'))


def format_project_ref_string(repo):
    """Return formatted project ref string

    :param GitRepo repo: Git repo
    :return: Formmatted repo ref
    :rtype: str
    """

    local_commits = repo.new_commits()
    upstream_commits = repo.new_commits(upstream=True)
    no_local_commits = local_commits == 0 or local_commits == '0'
    no_upstream_commits = upstream_commits == 0 or upstream_commits == '0'
    if no_local_commits and no_upstream_commits:
        status = ''
    else:
        local_commits_output = colored('+' + str(local_commits), 'yellow')
        upstream_commits_output = colored('-' + str(upstream_commits), 'red')
        status = '(' + local_commits_output + '/' + upstream_commits_output + ')'

    if repo.is_detached():
        current_ref = repo.sha(short=True)
        return colored('[HEAD @ ' + current_ref + ']', 'magenta')
    current_branch = repo.current_branch()
    return colored('[' + current_branch + ']', 'magenta') + status


def format_project_string(repo, path):
    """Return formatted project name

    :param GitRepo repo: Git repo
    :param str path: Relative project path
    :return: Formatted project name
    :rtype: str
    """

    if not existing_git_repository(repo.repo_path):
        return colored(path, 'green')
    if not repo.validate_repo():
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(path + symbol, color)


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached(print_output=True):
            return
        return func(*args, **kwargs)

    return wrapper


def print_validation(repo):
    """Print validation messages

    :param GitRepo repo: Git repo
    """

    if not existing_git_repository(repo.repo_path):
        return

    if not repo.validate_repo():
        print(' - Dirty repo. Please stash, commit, or discard your changes')
        repo.status_verbose()


def git_url(protocol, url, name):
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


def ref_type(ref):
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


def truncate_ref(ref):
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
