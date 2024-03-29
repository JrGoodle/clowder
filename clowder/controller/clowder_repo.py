"""Clowder repo utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from functools import wraps
from pathlib import Path
from typing import Optional, Tuple

import clowder.util.command as cmd
from clowder.util.console import CONSOLE
from clowder.util.format import Format
from clowder.util.git import ORIGIN, Repo

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import DuplicateVersionsError
from clowder.util.yaml import link_clowder_yaml


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_repo_dir.is_dir():
            CONSOLE.stdout(ClowderRepo(ENVIRONMENT.clowder_repo_dir).status)
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir:
            CONSOLE.stdout(ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).status)
        return func(*args, **kwargs)

    return wrapper


class ClowderRepo:
    """Class encapsulating git utilities for clowder repo

    :ivar str repo_path: Absolute path to repo
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, path: Path, remote: Optional[str] = None):
        """ProjectRepo __init__"""

        remote = ORIGIN if remote is None else remote
        self.path: Path = path
        self.repo: Repo = Repo(path, default_remote=remote)

    def branches(self) -> None:
        """Print current local branches"""

        self.repo.print_local_branches()
        self.repo.print_remote_branches()

    @classmethod
    def saved_version_names(cls) -> Optional[Tuple[str, ...]]:
        """Return list of all saved versions

        :return: All saved version names
        :raise DuplicateVersionsError:
        """

        if ENVIRONMENT.clowder_repo_versions_dir is None or not ENVIRONMENT.clowder_repo_versions_dir.exists():
            return None

        versions = [Path(Path(v).stem).stem for v in os.listdir(str(ENVIRONMENT.clowder_repo_versions_dir))
                    if v.endswith('.clowder.yml') or v.endswith('.clowder.yaml')]

        duplicate = fmt.check_for_duplicates(versions)
        if duplicate is not None:
            raise DuplicateVersionsError(f"Duplicate version found: {Format.path(Path(duplicate))}")

        return tuple(sorted(versions))

    def init(self, url: str, branch: Optional[str] = None) -> None:
        """Clone clowder repo from url

        :param str url: URL of repo to clone
        :param str branch: Branch to checkout
        :raise AmbiguousYamlError:
        """

        if self.repo.exists:
            raise Exception('Repo already exists')

        self.repo.clone(self.path, url, branch=branch)
        try:
            link_clowder_yaml(ENVIRONMENT.current_dir)
        except Exception:
            LOG.error('Failed to link yaml file after clowder repo init')
            raise
        else:
            if ENVIRONMENT.has_ambiguous_clowder_yaml_files():
                raise ENVIRONMENT.ambiguous_yaml_error

    # def create_clowder_repo(self, url: str, branch: str, depth: int = 0) -> None:
    #     """Clone clowder git repo from url at path
    #
    #     :param str url: URL of repo
    #     :param str branch: Branch name
    #     :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #     :raise ExistingFileError:
    #     """
    #
    #     if self.repo.exists:
    #         # TODO: Throw error if repo doesn't match one trying to create
    #         return
    #
    #     if self.repo_path.is_dir():
    #         try:
    #             self.repo_path.rmdir()
    #         except OSError:
    #             LOG.error(f"Directory already exists at {fmt.path(self.repo_path)}")
    #             raise
    #
    #     if self.repo_path.is_symlink():
    #         fs.remove_file(self.repo_path)
    #     else:
    #         from clowder.environment import ENVIRONMENT
    #         if ENVIRONMENT.existing_clowder_repo_file_error:
    #             raise ENVIRONMENT.existing_clowder_repo_file_error
    #
    #     self._init_repo()
    #     self._create_remote(self.remote, url, remove_dir=True)
    #     self._checkout_new_repo_branch(branch, depth)

    def formatted_name(self, color: bool = False) -> str:
        """Formatted project name"""

        output = '.clowder'

        if self.repo.is_dirty:
            output = f'{output}*'

        if not color:
            return output

        if '*' in output:
            return Format.red(output)
        return Format.green(output)

    def fetch(self) -> None:
        self.repo.default_remote.fetch(prune=True, tags=True)

    @property
    def status(self) -> Optional[str]:
        """Get clowder repo status"""

        if ENVIRONMENT.clowder_repo_dir is None:
            return None

        if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
            message = f"Found a {Format.path(ENVIRONMENT.clowder_yaml.name)} file but it is not a symlink " \
                      f"to a file stored in the existing {Format.path(Path('.clowder'))} repo"
            LOG.error(message)
            LOG.error()

        if ENVIRONMENT.clowder_git_repo_dir is None:
            output = Format.green(ENVIRONMENT.clowder_repo_dir.name)
        else:
            output = f"{self.formatted_name(color=True)} {self.repo.formatted_ref}"

        if ENVIRONMENT.clowder_yaml is not None and ENVIRONMENT.clowder_yaml.is_symlink():
            target_path = Format.path(Path(ENVIRONMENT.clowder_yaml.name))
            # FIXME: This can cause an error if symlink is pointing to existing file not relative to clowder dir
            source_path = Format.path(ENVIRONMENT.clowder_yaml.resolve().relative_to(ENVIRONMENT.clowder_dir))
            output += f"\n{target_path} -> {source_path}"

        return f'{output}\n'

    def run(self, command: str, check: bool = True) -> None:
        """Run command in clowder repo

        :param str command: Command to run
        :param bool check: Whether to check for errors
        """

        cmd.run(command, self.path, print_command=True, check=check)
