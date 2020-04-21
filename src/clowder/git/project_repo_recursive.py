# -*- coding: utf-8 -*-
"""Project Git utility class with submodules

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional

from git import GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.git.project_repo import ProjectRepo
from clowder.util.execute import execute_command


class ProjectRepoRecursive(ProjectRepo):
    """Class encapsulating git utilities for projects with submodules

    :ivar strt repo_path: Absolute path to repo
    :ivar strt default_ref: Default ref
    :ivar strt remote: Default remote name
    :ivar bool parallel: Whether command is being run in parallel, affects output
    :ivar Repo repo: Repo instance
    """

    def __init__(self, repo_path: str, remote: str, default_ref: str, parallel: bool = False):
        """ProjectRepoRecursive __init__

        :param str repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        :param bool parallel: Whether command is being run in parallel, affects output. Defaults to False
        """

        ProjectRepo.__init__(self, repo_path, remote, default_ref, parallel=parallel)

    def clean(self, args: str = '') -> None:
        """Discard changes for repo and submodules

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        """

        ProjectRepo.clean(self, args=args)

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

    def herd(self, url: str, depth: int = 0, fetch: bool = True, rebase: bool = False) -> None:
        """Herd ref

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        ProjectRepo.herd(self, url, depth=depth, fetch=fetch, rebase=rebase)
        self.submodule_update_recursive(depth)

    def herd_branch(self, url: str, branch: str, depth: int = 0, rebase: bool = False,
                    fork_remote: Optional[str] = None) -> None:
        """Herd branch

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[str] fork_remote: Fork remote name
        """

        ProjectRepo.herd_branch(self, url, branch, depth=depth, rebase=rebase, fork_remote=fork_remote)
        self.submodule_update_recursive(depth)

    def herd_tag(self, url: str, tag: str, depth: int = 0, rebase: bool = False) -> None:
        """Herd tag

        .. py:function:: herd_tag(url, tag, depth=0, rebase=False)

        :param str url: URL of repo
        :param str tag: Tag name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        ProjectRepo.herd_tag(self, url, tag, depth=depth, rebase=rebase)
        self.submodule_update_recursive(depth)

    def is_dirty_submodule(self, path: str) -> bool:
        """Check whether submodule repo is dirty

        :param str path: Submodule path
        :return: True, if submodule at path is dirty
        :rtype: bool
        """

        return not self.repo.is_dirty(path)

    def submodule_update_recursive(self, depth: int = 0) -> None:
        """Update submodules recursively and initialize if not present

        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._print(' - Recursively update and init submodules')

        if depth == 0:
            command = ['git', 'submodule', 'update', '--init', '--recursive']
        else:
            command = ['git', 'submodule', 'update', '--init', '--recursive', '--depth', depth]

        try:
            execute_command(command, self.repo_path)
        except ClowderError:
            message = colored(' - Failed to update submodules\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message)

    def sync(self, fork_remote: str, rebase: bool = False) -> None:
        """Sync fork with upstream remote

        :param str fork_remote: Fork remote name
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        ProjectRepo.sync(self, fork_remote, rebase=rebase)
        self.submodule_update_recursive()

    def validate_repo(self) -> bool:
        """Validate repo state

        :return: True, if repo and submodules not dirty or repo doesn't exist on disk
        :rtype: bool
        """

        if not ProjectRepo.validate_repo(self):
            return False

        return not any([self.is_dirty_submodule(s.path) for s in self.repo.submodules])

    def _submodules_clean(self) -> None:
        """Clean all submodules

        Equivalent to: ``git submodule foreach --recursive git clean -ffdx``
        """

        self._submodule_command('foreach', '--recursive', 'git', 'clean', '-ffdx',
                                error_msg=' - Failed to clean submodules')

    def _submodule_command(self, *args, error_msg: str) -> None:
        """Base submodule command

        :param str error_msg: Error message
        """

        try:
            self.repo.git.submodule(*args)
        except (GitError, ValueError) as err:
            message = colored(error_msg, 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _submodules_reset(self) -> None:
        """Reset all submodules

        Equivalent to: ``git submodule foreach --recursive git reset --hard``
        """

        self._submodule_command('foreach', '--recursive', 'git', 'reset', '--hard',
                                error_msg=' - Failed to reset submodules')

    def _submodules_update(self) -> None:
        """Update all submodules

        Equivalent to: ``git submodule update --checkout --recursive --force``
        """

        self._submodule_command('update', '--checkout', '--recursive', '--force',
                                error_msg=' - Failed to update submodules')
