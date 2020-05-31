# -*- coding: utf-8 -*-
"""Clowder repo utils

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from pathlib import Path
from typing import Optional, Tuple

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git import ProjectRepo
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory
from clowder.util.yaml import link_clowder_yaml_default


clowder_repo_ref = 'refs/heads/master'
clowder_repo_remote = 'origin'


def add(files: str) -> None:
    """Add files in clowder repo to git index

    :param str files: Files to git add
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    repo.add(files)


def branches() -> None:
    """Print current local branches"""

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    repo.print_local_branches()
    repo.print_remote_branches()


def checkout(ref: str) -> None:
    """Checkout ref in clowder repo

    :param str ref: Ref to git checkout
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    if repo.is_dirty():
        print(' - Dirty repo. Please stash, commit, or discard your changes')
        repo.status_verbose()
        return
    repo.checkout(ref)


def clean() -> None:
    """Discard changes in clowder repo

    Equivalent to: ``git clean -ffdx``
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    if repo.is_dirty():
        print(' - Discard current changes')
        repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
        repo.clean(args='fdx')
        return

    print(' - No changes to discard')


def commit(message: str) -> None:
    """Commit current changes in clowder repo

    :param str message: Git commit message
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    repo.commit(message)


def get_saved_version_names() -> Optional[Tuple[str, ...]]:
    """Return list of all saved versions

    :return: All saved version names
    :rtype: Optional[Tuple[str, ...]]
    :raise ClowderError:
    """

    if ENVIRONMENT.clowder_repo_versions_dir is None:
        return None

    versions = [Path(Path(v).stem).stem for v in os.listdir(str(ENVIRONMENT.clowder_repo_versions_dir))
                if v.endswith('.clowder.yml') or v.endswith('.clowder.yaml')]

    duplicate = fmt.check_for_duplicates(versions)
    if duplicate is not None:
        raise ClowderError(ClowderErrorType.DUPLICATE_SAVED_VERSIONS, fmt.error_duplicate_version(duplicate))

    return tuple(sorted(versions))


def git_status() -> None:
    """Print clowder repo git status

    Equivalent to: ``git status -vv``
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    repo.status_verbose()


def init(url: str, branch: str) -> None:
    """Clone clowder repo from url

    :param str url: URL of repo to clone
    :param str branch: Branch to checkout
    """

    clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
    try:
        repo = ProjectRepo(clowder_repo_dir, clowder_repo_remote, clowder_repo_ref)
        repo.create_clowder_repo(url, branch)
    except ClowderError as err:
        LOG_DEBUG('Failed to init clowder repo', err)
        if clowder_repo_dir.is_dir():
            remove_directory(clowder_repo_dir)
        raise ClowderError(ClowderErrorType.FAILED_INIT, fmt.error_failed_clowder_init(), err)
    except Exception as err:
        LOG_DEBUG('Failed to init clowder repo', err)
        if clowder_repo_dir.is_dir():
            remove_directory(clowder_repo_dir)
        raise ClowderError(ClowderErrorType.FAILED_INIT, fmt.error_failed_clowder_init(), err)
    else:
        try:
            link_clowder_yaml_default(ENVIRONMENT.current_dir)
        except ClowderError as err:
            LOG_DEBUG('Failed to link yaml file after clowder repo init', err)
            raise
        else:
            if ENVIRONMENT.has_ambiguous_clowder_yaml_files():
                raise ENVIRONMENT.ambiguous_clowder_yaml_error


def print_status(fetch: bool = False) -> None:
    """Print clowder repo status

    :param bool fetch: Fetch before printing status
    """

    if ENVIRONMENT.clowder_repo_dir is None:
        return

    clowder_repo_output = colored(ENVIRONMENT.clowder_repo_dir.name, 'green')

    if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
        print(fmt.warning_clowder_yaml_not_symlink_with_clowder_repo(ENVIRONMENT.clowder_yaml.name))
        print()

    symlink_output: Optional[str] = None
    if ENVIRONMENT.clowder_yaml is not None and ENVIRONMENT.clowder_yaml.is_symlink():
        target_path = fmt.path_string(Path(ENVIRONMENT.clowder_yaml.name))
        source_path = fmt.path_string(ENVIRONMENT.clowder_yaml.resolve().relative_to(ENVIRONMENT.clowder_dir))
        symlink_output = f"{target_path} -> {source_path}"

    if ENVIRONMENT.clowder_git_repo_dir is None:
        print(clowder_repo_output)
        if symlink_output is not None:
            print(symlink_output)
        print()
        return

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)

    if fetch and not is_offline():
        print(' - Fetch upstream changes for clowder repo')
        repo.fetch(clowder_repo_remote)

    clowder_git_repo_output = repo.format_project_string(ENVIRONMENT.clowder_git_repo_dir.name)
    current_ref_output = repo.format_project_ref_string()

    print(f"{clowder_git_repo_output} {current_ref_output}")
    if symlink_output is not None:
        print(symlink_output)
    print()


def pull() -> None:
    """Pull clowder repo upstream changes"""

    ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref).pull()


def push() -> None:
    """Push clowder repo changes"""

    ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref).push()


def run_command(command: str) -> None:
    """Run command in clowder repo

    :param str command: Command to run
    """

    print(fmt.command(command))
    execute_command(command.split(), ENVIRONMENT.clowder_repo_dir)
