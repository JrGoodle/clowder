"""Clowder repo utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from functools import wraps
from pathlib import Path
from typing import Optional, Tuple

import pygoodle.command as cmd
from pygoodle.connectivity import is_offline
from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.git import LocalBranch, Repo

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import DuplicateVersionsError
from clowder.util.yaml import link_clowder_yaml_default


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_repo_dir.is_dir():
            ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir:
            ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).print_status(fetch=True)
        return func(*args, **kwargs)

    return wrapper


class ClowderRepo(Repo):
    """Class encapsulating git utilities for clowder repo

    :ivar str repo_path: Absolute path to repo
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, path: Path, remote: str = 'origin'):
        """ProjectRepo __init__"""

        super().__init__(path, remote)

    def branches(self) -> None:
        """Print current local branches"""

        self.print_local_branches()
        self.print_remote_branches()

    @classmethod
    def get_saved_version_names(cls) -> Optional[Tuple[str, ...]]:
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

    def init(self, url: str, branch: str) -> None:
        """Clone clowder repo from url

        :param str url: URL of repo to clone
        :param str branch: Branch to checkout
        :raise AmbiguousYamlError:
        """

        if self.exists:
            raise Exception('Repo already exists')

        branch = LocalBranch(self.path, branch)
        self.clone(self.path, url, ref=branch)
        try:
            link_clowder_yaml_default(ENVIRONMENT.current_dir)
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

    def formatted_name(self, padding: Optional[int] = None, color: bool = False) -> str:
        """Formatted project name"""

        output = '.clowder'
        if not self.exists:
            if color:
                return Format.green(output)
            return output

        if self.is_dirty:
            output = f'{output}*'

        if padding is not None:
            output = output.ljust(padding)

        if not color:
            return output

        if '*' in output:
            return Format.red(output)
        return Format.green(output)

    def print_status(self, fetch: bool = False) -> None:
        """Print clowder repo status

        :param bool fetch: Fetch before printing status
        """

        if ENVIRONMENT.clowder_repo_dir is None:
            return

        if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
            message = f"Found a {Format.path(ENVIRONMENT.clowder_yaml.name)} file but it is not a symlink " \
                      f"to a file stored in the existing {Format.path(Path('.clowder'))} repo"
            LOG.error(message)
            LOG.error()

        symlink_output: Optional[str] = None
        if ENVIRONMENT.clowder_yaml is not None and ENVIRONMENT.clowder_yaml.is_symlink():
            target_path = Format.path(Path(ENVIRONMENT.clowder_yaml.name))
            # FIXME: This can cause an error if symlink is pointing to existing file not relative to clowder dir
            source_path = Format.path(ENVIRONMENT.clowder_yaml.resolve().relative_to(ENVIRONMENT.clowder_dir))
            symlink_output = f"{target_path} -> {source_path}"

        if ENVIRONMENT.clowder_git_repo_dir is None:
            CONSOLE.stdout(Format.green(ENVIRONMENT.clowder_repo_dir.name))
            if symlink_output is not None:
                CONSOLE.stdout(symlink_output)
            CONSOLE.stdout()
            return

        if fetch and not is_offline():
            CONSOLE.stdout(' - Fetch upstream changes for clowder repo')
            self.default_remote.fetch(prune=True, tags=True)

        CONSOLE.stdout(f"{self.formatted_name(color=True)} {self.formatted_ref}")
        if symlink_output is not None:
            CONSOLE.stdout(symlink_output)
        CONSOLE.stdout()

    def run(self, command: str, check: bool = True) -> None:
        """Run command in clowder repo

        :param str command: Command to run
        :param bool check: Whether to check for errors
        """

        cmd.run(command, self.path, print_command=True, check=check)
