# -*- coding: utf-8 -*-
"""Clowder repo utils

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import atexit
import os
from pathlib import Path

from termcolor import colored

import clowder.util.formatting as fmt
from clowder import CLOWDER_DIR, CLOWDER_REPO_DIR, CLOWDER_YAML, CURRENT_DIR
from clowder.error import ClowderError, ClowderExit
from clowder.git import ProjectRepo
from clowder.git.util import existing_git_repository
from clowder.util.clowder_utils import link_clowder_yaml_default
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory


clowder_repo_ref: str = 'refs/heads/master'
clowder_repo_remote: str = 'origin'


def add(files: str) -> None:
    """Add files in clowder repo to git index

    :param str files: Files to git add
    """

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    repo.add(files)


def branches() -> None:
    """Print current local branches"""

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    repo.print_local_branches()
    repo.print_remote_branches()


def checkout(ref: str) -> None:
    """Checkout ref in clowder repo

    :param str ref: Ref to git checkout
    """

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    if repo.is_dirty():
        print(' - Dirty repo. Please stash, commit, or discard your changes')
        repo.status_verbose()
        return
    repo.checkout(ref)


def clean() -> None:
    """Discard changes in clowder repo

    Equivalent to: ``git clean -ffdx``
    """

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    if repo.is_dirty():
        print(' - Discard current changes')
        repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
        repo.clean(args='fdx')
        return

    print(' - No changes to discard')


def commit(message: str) -> None:
    """Commit current changes in clowder repo

    :param str message: Git commit message
    """

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    repo.commit(message)


def git_status() -> None:
    """Print clowder repo git status

    Equivalent to: ``git status -vv``
    """

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)
    repo.status_verbose()


def init(url: str, branch: str) -> None:
    """Clone clowder repo from url

    :param str url: URL of repo to clone
    :param str branch: Branch to checkout
    """

    # Register exit handler to remove files if cloning repo fails
    atexit.register(_init_exit_handler)

    clowder_repo_dir = CURRENT_DIR / '.clowder'
    repo = ProjectRepo(clowder_repo_dir, clowder_repo_remote, clowder_repo_ref)
    repo.create_clowder_repo(url, branch)
    link_clowder_yaml_default(CURRENT_DIR)


def print_status(fetch: bool = False) -> None:
    """Print clowder repo status

    :param bool fetch: Fetch before printing status
    """

    if not existing_git_repository(CLOWDER_REPO_DIR):
        output = colored('.clowder', 'green')
        print(output)
        return

    repo = ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref)

    if not is_offline() and fetch:
        print(' - Fetch upstream changes for clowder repo')
        repo.fetch(clowder_repo_remote)

    clowder_path = Path('.clowder')
    project_output = repo.format_project_string(clowder_path)
    current_ref_output = repo.format_project_ref_string()

    if CLOWDER_YAML is None or not CLOWDER_YAML.is_symlink():
        print(f"{project_output} {current_ref_output}")
        return

    symlink_path = fmt.path_string(Path(CLOWDER_YAML.name))
    file_path = fmt.path_string(CLOWDER_YAML.resolve().relative_to(CLOWDER_DIR))
    print(f"{project_output} {current_ref_output}")
    print(f"{symlink_path} -> {file_path}\n")


def pull() -> None:
    """Pull clowder repo upstream changes"""

    ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref).pull()


def push() -> None:
    """Push clowder repo changes"""

    ProjectRepo(CLOWDER_REPO_DIR, clowder_repo_remote, clowder_repo_ref).push()


def run_command(command: str) -> None:
    """Run command in clowder repo

    :param str command: Command to run
    :raise ClowderError:
    """

    print(fmt.command(command))
    try:
        execute_command(command.split(), CLOWDER_REPO_DIR)
    except ClowderError as err:
        print(fmt.error_command_failed(command))
        raise err


def _init_exit_handler() -> None:
    """Exit handler for deleting files if clowder init fails

    :raise ClowderExit:
    """

    clowder_path = CURRENT_DIR / '.clowder'
    if os.path.isdir(clowder_path):
        clowder_yml = CURRENT_DIR / 'clowder.yml'
        clowder_yaml = CURRENT_DIR / 'clowder.yaml'
        if not clowder_yml.is_symlink() and not clowder_yaml.is_symlink():
            remove_directory(clowder_path)
            raise ClowderExit(1)
