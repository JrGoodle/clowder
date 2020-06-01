# -*- coding: utf-8 -*-
"""Project Git utility class with submodules

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from git import GitError

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.util.execute import execute_command

from .project_repo import GitConfig, ProjectRepo


class ProjectRepoRecursive(ProjectRepo):
    """Class encapsulating git utilities for projects with submodules

    :ivar strt repo_path: Absolute path to repo
    :ivar strt default_ref: Default ref
    :ivar strt remote: Default remote name
    :ivar bool parallel: Whether command is being run in parallel, affects output
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str, default_ref: str, parallel: bool = False):
        """ProjectRepoRecursive __init__

        :param Path repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        :param bool parallel: Whether command is being run in parallel, affects output. Defaults to False
        """

        super().__init__(repo_path, remote, default_ref, parallel=parallel)

    def clean(self, args: str = '') -> None:
        """Discard changes for repo and submodules

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        """

        super().clean(args=args)

        self._print(' - Clean submodules recursively')
        self._submodules_clean()

        self._print(' - Reset submodules recursively')
        self._submodules_reset()

        self._print(' - Update submodules recursively')
        self._submodules_update()

    def has_submodules(self) -> bool:
        """Repo has submodules

        :return: True, if repo has submodules
        :rtype: bool
        """

        return len(self.repo.submodules) > 0

    def herd(self, url: str, depth: int = 0, fetch: bool = True,
             rebase: bool = False, config: Optional[GitConfig] = None) -> None:
        """Herd ref

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[GitConfig] config: Custom git config
        """

        super().herd(url, depth=depth, fetch=fetch, rebase=rebase, config=config)
        self.submodule_update_recursive(depth)

    def herd_branch(self, url: str, branch: str, depth: int = 0, rebase: bool = False,
                    fork_remote: Optional[str] = None, config: Optional[GitConfig] = None) -> None:
        """Herd branch

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[str] fork_remote: Fork remote name
        :param Optional[GitConfig] config: Custom git config
        """

        super().herd_branch(url, branch, depth=depth, rebase=rebase, fork_remote=fork_remote, config=config)
        self.submodule_update_recursive(depth)

    def herd_tag(self, url: str, tag: str, depth: int = 0,
                 rebase: bool = False, config: Optional[GitConfig] = None) -> None:
        """Herd tag

        :param str url: URL of repo
        :param str tag: Tag name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[GitConfig] config: Custom git config
        """

        super().herd_tag(url, tag, depth=depth, rebase=rebase, config=config)
        self.submodule_update_recursive(depth)

    def is_dirty_submodule(self, path: str) -> bool:
        """Check whether submodule repo is dirty

        :param str path: Submodule path
        :return: True, if submodule at path is dirty
        :rtype: bool
        """

        return self.repo.is_dirty(path)

    def submodule_update_recursive(self, depth: int = 0) -> None:
        """Update submodules recursively and initialize if not present

        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._print(' - Recursively update and init submodules')

        if depth == 0:
            command = f"git submodule update --init --recursive"
        else:
            command = f"git submodule update --init --recursive --depth {depth}"

        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError as err:
            LOG_DEBUG('Failed to update submodules', err)
            message = f'{fmt.ERROR} Failed to update submodules'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def validate_repo(self, allow_missing_repo: bool = True) -> bool:
        """Validate repo state

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        :return: True, if repo and submodules not dirty or repo doesn't exist on disk
        :rtype: bool
        """

        if not super().validate_repo(allow_missing_repo=allow_missing_repo):
            return False

        return not any([self.is_dirty_submodule(s.path) for s in self.repo.submodules])

    def _submodules_clean(self) -> None:
        """Clean all submodules

        Equivalent to: ``git submodule foreach --recursive git clean -ffdx``
        """

        self._submodule_command('foreach', '--recursive', 'git', 'clean', '-ffdx',
                                error_msg=f'{fmt.ERROR} Failed to clean submodules')

    def _submodule_command(self, *args, error_msg: str) -> None:
        """Base submodule command

        :param str error_msg: Error message
        :raise ClowderError:
        """

        try:
            self.repo.git.submodule(*args)
        except (GitError, ValueError) as err:
            LOG_DEBUG('Git error', err)
            message = self._format_error_message(error_msg)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _submodules_reset(self) -> None:
        """Reset all submodules

        Equivalent to: ``git submodule foreach --recursive git reset --hard``
        """

        self._submodule_command('foreach', '--recursive', 'git', 'reset', '--hard',
                                error_msg=f'{fmt.ERROR} Failed to reset submodules')

    def _submodules_update(self) -> None:
        """Update all submodules

        Equivalent to: ``git submodule update --checkout --recursive --force``
        """

        self._submodule_command('update', '--checkout', '--recursive', '--force',
                                error_msg=f'{fmt.ERROR} Failed to update submodules')
