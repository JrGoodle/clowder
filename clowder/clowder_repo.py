"""Clowder repo utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from pathlib import Path
from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git_project import ProjectRepo
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
    if repo.is_dirty:
        CONSOLE.stdout(' - Dirty repo. Please stash, commit, or discard your changes')
        repo.status_verbose()
        return
    repo.checkout(ref)


def clean() -> None:
    """Discard changes in clowder repo

    Equivalent to: ``git clean -ffdx``
    """

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
    if repo.is_dirty:
        CONSOLE.stdout(' - Discard current changes')
        repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)
        repo.clean(args='fdx')
        return

    CONSOLE.stdout(' - No changes to discard')


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

    if not ENVIRONMENT.clowder_repo_versions_dir.exists():
        return None

    versions = [Path(Path(v).stem).stem for v in os.listdir(str(ENVIRONMENT.clowder_repo_versions_dir))
                if v.endswith('.clowder.yml') or v.endswith('.clowder.yaml')]

    duplicate = fmt.check_for_duplicates(versions)
    if duplicate is not None:
        message = f"Duplicate version found: {fmt.yaml_file(Path(duplicate))}"
        raise ClowderError(ClowderErrorType.DUPLICATE_SAVED_VERSIONS, message)

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
    error_message = "Failed to initialize clowder repo"
    try:
        repo = ProjectRepo(clowder_repo_dir, clowder_repo_remote, clowder_repo_ref)
        repo.create_clowder_repo(url, branch)
    except ClowderError:
        if clowder_repo_dir.is_dir():
            remove_directory(clowder_repo_dir)
        CONSOLE.stderr(error_message)
        raise
    except Exception:
        if clowder_repo_dir.is_dir():
            remove_directory(clowder_repo_dir)
        CONSOLE.stderr(error_message)
        raise
    else:
        try:
            link_clowder_yaml_default(ENVIRONMENT.current_dir)
        except ClowderError:
            CONSOLE.stderr('Failed to link yaml file after clowder repo init')
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

    clowder_repo_output = fmt.green(ENVIRONMENT.clowder_repo_dir.name)

    if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
        message = f"Found a {fmt.yaml_file(ENVIRONMENT.clowder_yaml.name)} file but it is not a symlink " \
                  f"to a file stored in the existing {fmt.path(Path('.clowder'))} repo"
        CONSOLE.stderr(message)
        CONSOLE.stderr()

    symlink_output: Optional[str] = None
    if ENVIRONMENT.clowder_yaml is not None and ENVIRONMENT.clowder_yaml.is_symlink():
        target_path = fmt.path(Path(ENVIRONMENT.clowder_yaml.name))
        # FIXME: This can cause an error if symlink is pointing to existing file not relative to clowder dir
        source_path = fmt.path(ENVIRONMENT.clowder_yaml.resolve().relative_to(ENVIRONMENT.clowder_dir))
        symlink_output = f"{target_path} -> {source_path}"

    if ENVIRONMENT.clowder_git_repo_dir is None:
        CONSOLE.stdout(clowder_repo_output)
        if symlink_output is not None:
            CONSOLE.stdout(symlink_output)
        CONSOLE.stdout()
        return

    repo = ProjectRepo(ENVIRONMENT.clowder_git_repo_dir, clowder_repo_remote, clowder_repo_ref)

    if fetch and not is_offline():
        CONSOLE.stdout(' - Fetch upstream changes for clowder repo')
        repo.fetch(clowder_repo_remote)

    clowder_git_repo_output = repo.format_project_string(ENVIRONMENT.clowder_git_repo_dir.name)
    CONSOLE.stdout(f"{clowder_git_repo_output} {repo.formatted_ref}")
    if symlink_output is not None:
        CONSOLE.stdout(symlink_output)
    CONSOLE.stdout()


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

    CONSOLE.stdout(fmt.command(command))
    execute_command(command.split(), ENVIRONMENT.clowder_repo_dir)
