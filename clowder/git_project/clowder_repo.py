"""Clowder repo utils

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from pathlib import Path
from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.environment import ENVIRONMENT
from clowder.error import *
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
# from clowder.util.file_system import remove_directory
from clowder.util.yaml import link_clowder_yaml_default


from .git_ref import GitRef
from .project_repo import ProjectRepo


class ClowderRepo(ProjectRepo):
    """Class encapsulating git utilities for clowder repo

    :ivar str repo_path: Absolute path to repo
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str = 'origin', default_ref: GitRef = GitRef(branch='master')):
        """ProjectRepo __init__"""

        super().__init__(repo_path, remote, default_ref)

    def add(self, files: str) -> None:
        """Add files in clowder repo to git index

        :param str files: Files to git add
        """

        super().add(files)

    def branches(self) -> None:
        """Print current local branches"""

        self.print_local_branches()
        self.print_remote_branches()

    def checkout(self, ref: str, allow_failure: bool = False) -> None:
        """Checkout ref in clowder repo

        :param str ref: Ref to git checkout
        :param bool allow_failure: Whether to allow failing to checkout branch
        """

        if self.is_dirty:
            CONSOLE.stdout(' - Dirty repo. Please stash, commit, or discard your changes')
            self.status_verbose()
            return
        super().checkout(ref)

    def clean(self, args: str = 'fdx') -> None:
        """Discard changes in clowder repo

        Equivalent to: ``git clean -ffdx``
        """

        if self.is_dirty:
            CONSOLE.stdout(' - Discard current changes')
            super().clean(args=args)
            return

        CONSOLE.stdout(' - No changes to discard')

    def commit(self, message: str) -> None:
        """Commit current changes in clowder repo

        :param str message: Git commit message
        """

        super().commit(message)

    @staticmethod
    def get_saved_version_names() -> Optional[Tuple[str, ...]]:
        """Return list of all saved versions

        :return: All saved version names
        :raise DuplicateVersionsError:
        """

        if ENVIRONMENT.clowder_repo_versions_dir is None:
            return None

        if not ENVIRONMENT.clowder_repo_versions_dir.exists():
            return None

        versions = [Path(Path(v).stem).stem for v in os.listdir(str(ENVIRONMENT.clowder_repo_versions_dir))
                    if v.endswith('.clowder.yml') or v.endswith('.clowder.yaml')]

        duplicate = fmt.check_for_duplicates(versions)
        if duplicate is not None:
            raise DuplicateVersionsError(f"Duplicate version found: {fmt.path(Path(duplicate))}")

        return tuple(sorted(versions))

    def git_status(self) -> None:
        """Print clowder repo git status

        Equivalent to: ``git status -vv``
        """

        self.status_verbose()

    def init(self, url: str, branch: str) -> None:
        """Clone clowder repo from url

        :param str url: URL of repo to clone
        :param str branch: Branch to checkout
        :raise AmbiguousYamlError:
        """

        try:
            self.create_clowder_repo(url, branch)
        except BaseException:
            # if self.repo_path.is_dir():
            #     remove_directory(self.repo_path, check=False)
            CONSOLE.stderr("Failed to initialize clowder repo")
            raise
        else:
            try:
                link_clowder_yaml_default(ENVIRONMENT.current_dir)
            except Exception:
                CONSOLE.stderr('Failed to link yaml file after clowder repo init')
                raise
            else:
                if ENVIRONMENT.has_ambiguous_clowder_yaml_files():
                    raise ENVIRONMENT.ambiguous_clowder_yaml_error

    def print_status(self, fetch: bool = False) -> None:
        """Print clowder repo status

        :param bool fetch: Fetch before printing status
        """

        if ENVIRONMENT.clowder_repo_dir is None:
            return

        if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
            message = f"Found a {fmt.path(ENVIRONMENT.clowder_yaml.name)} file but it is not a symlink " \
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
            CONSOLE.stdout(fmt.green(ENVIRONMENT.clowder_repo_dir.name))
            if symlink_output is not None:
                CONSOLE.stdout(symlink_output)
            CONSOLE.stdout()
            return

        if fetch and not is_offline():
            CONSOLE.stdout(' - Fetch upstream changes for clowder repo')
            self.fetch(self.remote)

        clowder_git_repo_output = self.format_project_string(ENVIRONMENT.clowder_git_repo_dir.name)
        CONSOLE.stdout(f"{clowder_git_repo_output} {self.formatted_ref}")
        if symlink_output is not None:
            CONSOLE.stdout(symlink_output)
        CONSOLE.stdout()

    def pull(self) -> None:
        """Pull clowder repo upstream changes"""

        super().pull()

    def push(self) -> None:
        """Push clowder repo changes"""

        super().push()

    def run_command(self, command: str) -> None:
        """Run command in clowder repo

        :param str command: Command to run
        """

        CONSOLE.stdout(fmt.command(command))
        execute_command(command.split(), self.repo_path)
