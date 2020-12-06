"""Clowder git utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional

import pygoodle.filesystem as fs
from pygoodle.console import CONSOLE
from pygoodle.formatting import Format

from clowder.app import LOG
from clowder.util.execute import execute_command


def existing_git_repo(path: Path) -> bool:
    """Check if a git repository exists

    :param Path path: Repo path
    :return: True, if .git directory exists inside path
    """

    return path.is_dir() and Path(path / '.git').is_dir()


def existing_git_submodule(path: Path) -> bool:
    """Check if a git submodule exists

    :param Path path: Submodule path
    :return: True, if .git file exists inside path
    """

    return Path(path / '.git').is_file()


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached:
            CONSOLE.stdout(' - HEAD is detached')
            return
        return func(*args, **kwargs)

    return wrapper


def get_default_branch(repo_path: Path, remote: str, url: str) -> str:
    """Get default branch"""

    # FIXME: Need to distinguish between project and upstream
    # Upstream shouldn't save to disk, unless there's a convention for that
    if existing_git_repo(repo_path):
        default_branch = get_default_branch_from_local(repo_path, remote)
        if default_branch is not None:
            return default_branch

    default_branch = get_default_branch_from_remote(url)
    if default_branch is not None:
        save_default_branch(repo_path, remote, url)
        return default_branch

    return 'master'


def save_default_branch(repo_path: Path, remote: str, branch: str) -> None:
    """Save default branch"""

    git_dir = repo_path / '.git'
    if not git_dir.exists():
        return
    remote_head_ref = git_dir / 'refs' / 'remotes' / remote / 'HEAD'
    if not remote_head_ref.exists():
        fs.make_dir(remote_head_ref.parent)
        contents = f'ref: refs/remotes/{remote}/{branch}'
        remote_head_ref.touch()
        remote_head_ref.write_text(contents)


def get_default_branch_from_local(repo_path: Path, remote: str) -> Optional[str]:
    """Get default branch from local repo"""

    try:
        command = ['git', 'symbolic-ref', f'refs/remotes/{remote}/HEAD']
        result = execute_command(command, repo_path, print_output=False)
        output: str = result.stdout
        output_list = output.split()
        branch = [Format.remove_prefix(chunk, f'refs/remotes/{remote}/') for chunk in output_list
                  if chunk.startswith(f'refs/remotes/{remote}/')]
        return branch[0]
    except CalledProcessError as err:
        LOG.debug('Failed to get default branch from local git repo', err)
        return None


def get_default_branch_from_remote(url: str) -> Optional[str]:
    """Get default branch from remote repo"""

    try:
        command = ['git', 'ls-remote', '--symref', url, 'HEAD']
        result = execute_command(command, Path.cwd(), print_output=False)
        output: str = result.stdout
        output_list = output.split()
        branch = [Format.remove_prefix(chunk, 'refs/heads/')
                  for chunk in output_list if chunk.startswith('refs/heads/')]
        return branch[0]
    except CalledProcessError as err:
        LOG.debug('Failed to get default branch from remote git repo', err)
        return None
