# -*- coding: utf-8 -*-
"""Project Git utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from git import GitError

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.util.file_system import remove_file
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import is_offline

from .project_repo_impl import GitConfig, ProjectRepoImpl
from .util import (
    existing_git_repository,
    ref_type,
    truncate_ref
)


class ProjectRepo(ProjectRepoImpl):
    """Class encapsulating git utilities for projects

    :ivar str repo_path: Absolute path to repo
    :ivar str default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar bool parallel: Whether command is being run in parallel, affects output
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str, default_ref: str, parallel: bool = False):
        """ProjectRepo __init__

        :param Path repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        :param bool parallel: Whether command is being run in parallel, affects output. Defaults to False
        """

        super().__init__(repo_path, remote, default_ref, parallel=parallel)

    def create_clowder_repo(self, url: str, branch: str, depth: int = 0) -> None:
        """Clone clowder git repo from url at path

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        if existing_git_repository(self.repo_path):
            # TODO: Throw error if repo doesn't match one trying to create
            return

        if self.repo_path.is_dir():
            try:
                self.repo_path.rmdir()
            except OSError as err:
                LOG_DEBUG('Failed to remove existing .clowder directory', err)
                raise ClowderError(ClowderErrorType.DIRECTORY_EXISTS,
                                   fmt.error_directory_exists(str(self.repo_path)),
                                   error=err)

        if self.repo_path.is_symlink():
            remove_file(self.repo_path)
        else:
            from clowder.environment import ENVIRONMENT
            if ENVIRONMENT.clowder_repo_existing_file_error:
                raise ENVIRONMENT.clowder_repo_existing_file_error

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, upstream_remote_name: str, upstream_remote_url: str,
                          fork_remote_name: str, fork_remote_url: str) -> None:
        """Configure remotes names for fork and upstream

        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        :param str fork_remote_name: Fork remote name
        :param str fork_remote_url: Fork remote url
        :raise ClowderError:
        """

        if not existing_git_repository(self.repo_path):
            return

        try:
            remotes = self.repo.remotes
        except GitError as err:
            LOG_DEBUG('Git error', err)
            return
        else:
            for remote in remotes:
                if upstream_remote_url == self._remote_get_url(remote.name) and remote.name != upstream_remote_name:
                    self._rename_remote(remote.name, upstream_remote_name)
                    continue
                if fork_remote_url == self._remote_get_url(remote.name) and remote.name != fork_remote_name:
                    self._rename_remote(remote.name, fork_remote_name)
            self._compare_remotes(upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url)

    def herd(self, url: str, depth: int = 0, fetch: bool = True,
             rebase: bool = False, config: Optional[GitConfig] = None) -> None:
        """Herd ref

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[GitConfig] config: Custom git config
        """

        if not existing_git_repository(self.repo_path):
            self._herd_initial(url, depth=depth)
            self.install_project_git_herd_alias()
            if config is not None:
                self._update_git_config(config)
            return

        self.install_project_git_herd_alias()
        if config is not None:
            self._update_git_config(config)
        self._create_remote(self.remote, url)
        self._herd(self.remote, self.default_ref, depth=depth, fetch=fetch, rebase=rebase)

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

        if not existing_git_repository(self.repo_path):
            self._herd_branch_initial(url, branch, depth=depth)
            self.install_project_git_herd_alias()
            if config is not None:
                self._update_git_config(config)
            return

        if config is not None:
            self.install_project_git_herd_alias()
            self._update_git_config(config)

        branch_output = fmt.ref_string(branch)
        branch_ref = f'refs/heads/{branch}'
        if self.existing_local_branch(branch):
            self._herd_branch_existing_local(branch, depth=depth, rebase=rebase, fork_remote=fork_remote)
            return

        self.fetch(self.remote, depth=depth, ref=branch_ref, allow_failure=True)
        if self.existing_remote_branch(branch, self.remote):
            self._herd(self.remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return

        remote_output = fmt.remote_string(self.remote)
        self._print(f' - No existing remote branch {remote_output} {branch_output}')
        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd(fork_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return

            remote_output = fmt.remote_string(fork_remote)
            self._print(f' - No existing remote branch {remote_output} {branch_output}')

        fetch = depth != 0
        self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_tag(self, url: str, tag: str, depth: int = 0,
                 rebase: bool = False, config: Optional[GitConfig] = None) -> None:
        """Herd tag

        :param str url: URL of repo
        :param str tag: Tag name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[GitConfig] config: Custom git config
        """

        if not existing_git_repository(self.repo_path):
            self._init_repo()
            self._create_remote(self.remote, url, remove_dir=True)
            try:
                self._checkout_new_repo_tag(tag, self.remote, depth)
            except ClowderError as err:
                LOG_DEBUG('Failed checkout new repo tag', err)
                fetch = depth != 0
                self.herd(url, depth=depth, fetch=fetch, rebase=rebase)
                return
            else:
                self.install_project_git_herd_alias()
                if config is not None:
                    self._update_git_config(config)

        self.install_project_git_herd_alias()
        if config is not None:
            self._update_git_config(config)
        try:
            self.fetch(self.remote, ref=f'refs/tags/{tag}', depth=depth)
            self._checkout_tag(tag)
        except ClowderError as err:
            LOG_DEBUG('Failed fetch and checkout tag', err)
            fetch = depth != 0
            self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_remote(self, url: str, remote: str, branch: Optional[str] = None) -> None:
        """Herd remote repo

        :param str url: URL of repo
        :param str remote: Remote name
        :param Optional[str] branch: Branch name
        """

        self._create_remote(remote, url)

        if branch is None:
            self.fetch(remote, ref=self.default_ref)
            return

        try:
            self.fetch(remote, ref=branch)
        except ClowderError as err:
            LOG_DEBUG('Failed fetch', err)
            self.fetch(remote, ref=self.default_ref)

    def install_project_git_herd_alias(self) -> None:
        """Install 'git herd' alias for project"""

        from clowder.environment import ENVIRONMENT
        config_variable = 'alias.herd'
        config_value = f'!clowder herd {self.repo_path.relative_to(ENVIRONMENT.clowder_dir)}'
        self._print(" - Update git herd alias")
        self.git_config_unset_all_local(config_variable)
        self.git_config_add_local(config_variable, config_value)

    def prune_branch_local(self, branch: str, force: bool) -> None:
        """Prune local branch

        :param str branch: Branch name to delete
        :param bool force: Force delete branch
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        if branch not in self.repo.heads:
            self._print(f" - Local branch {branch_output} doesn't exist")
            return

        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = fmt.ref_string(truncate_ref(self.default_ref))
            try:
                self._print(f' - Checkout ref {ref_output}')
                self.repo.git.checkout(truncate_ref(self.default_ref))
            except GitError as err:
                LOG_DEBUG('Git error', err)
                message = f'{fmt.ERROR} Failed to checkout ref {ref_output}'
                message = self._format_error_message(message)
                raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

        try:
            self._print(f' - Delete local branch {branch_output}')
            self.repo.delete_head(branch, force=force)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to delete local branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def prune_branch_remote(self, branch: str, remote: str) -> None:
        """Prune remote branch in repository

        :param str branch: Branch name to delete
        :param str remote: Remote name
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        if not self.existing_remote_branch(branch, remote):
            self._print(f" - Remote branch {branch_output} doesn't exist")
            return

        try:
            self._print(f' - Delete remote branch {branch_output}')
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to delete remote branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def reset(self, depth: int = 0) -> None:
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        if ref_type(self.default_ref) == 'tag':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_tag(truncate_ref(self.default_ref))
            return

        if ref_type(self.default_ref) == 'sha':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_sha(self.default_ref)
            return

        branch = truncate_ref(self.default_ref)
        if not self.existing_local_branch(branch):
            self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=True)
            return

        self._checkout_branch(branch)

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(self.remote)
        if not self.existing_remote_branch(branch, self.remote):
            message = f'{fmt.ERROR} No existing remote branch {remote_output} {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        self.fetch(self.remote, ref=self.default_ref, depth=depth)
        self._print(f' - Reset branch {branch_output} to {remote_output} {branch_output}')
        remote_branch = f'{self.remote}/{branch}'
        self._reset_head(branch=remote_branch)

    def reset_timestamp(self, timestamp: str, author: str, ref: str) -> None:
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        :raise ClowderError:
        """

        rev = None
        if author:
            rev = self._find_rev_by_timestamp_author(timestamp, author, ref)
        if not rev:
            rev = self._find_rev_by_timestamp(timestamp, ref)
        if not rev:
            message = f'{fmt.ERROR} Failed to find revision'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        self._checkout_sha(rev)

    def start(self, remote: str, branch: str, depth: int, tracking: bool) -> None:
        """Start new branch in repository and checkout

        :param str remote: Remote name
        :param str branch: Local branch name to create
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool tracking: Whether to create a remote branch with tracking relationship
        :raise ClowderError:
        """

        if branch not in self.repo.heads:
            if not is_offline():
                self.fetch(remote, ref=branch, depth=depth)
            try:
                self._create_branch_local(branch)
                self._checkout_branch_local(branch)
            except ClowderError as err:
                LOG_DEBUG('Failed to create and checkout branch', err)
                raise
        else:
            self._print(f' - {fmt.ref_string(branch)} already exists')
            if self._is_branch_checked_out(branch):
                self._print(' - On correct branch')
            else:
                try:
                    self._checkout_branch_local(branch)
                except ClowderError as err:
                    LOG_DEBUG('Failed to checkout local branch', err)
                    raise

        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def _compare_remotes(self, upstream_remote_name: str, upstream_remote_url: str,
                         fork_remote_name: str, fork_remote_url: str) -> None:
        """Compare remotes names for fork and upstream

        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        :param str fork_remote_name: Fork remote name
        :param str fork_remote_url: Fork remote url
        """

        remote_names = [r.name for r in self.repo.remotes]
        if upstream_remote_name in remote_names:
            self._compare_remote_url(upstream_remote_name, upstream_remote_url)
        if fork_remote_name in remote_names:
            self._compare_remote_url(fork_remote_name, fork_remote_url)

    def _herd(self, remote: str, ref: str, depth: int = 0, fetch: bool = True, rebase: bool = False) -> None:
        """Herd ref

        :param str remote: Remote name
        :param str ref: Git ref
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        if ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(truncate_ref(ref))
            return

        if ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)
            return

        branch = truncate_ref(ref)
        if not self.existing_local_branch(branch):
            self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
            return

        self._herd_existing_local(remote, branch, depth=depth, rebase=rebase)

    def _herd_branch_existing_local(self, branch: str, depth: int = 0, rebase: bool = False,
                                    fork_remote: Optional[str] = None) -> None:
        """Herd branch for existing local branch

        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[str] fork_remote: Fork remote name
        """

        self._checkout_branch(branch)

        branch_ref = f'refs/heads/{branch}'
        self.fetch(self.remote, depth=depth, ref=branch_ref)
        if self.existing_remote_branch(branch, self.remote):
            self._herd_remote_branch(self.remote, branch, depth=depth, rebase=rebase)
            return

        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd_remote_branch(fork_remote, branch, depth=depth, rebase=rebase)

    def _herd_branch_initial(self, url: str, branch: str, depth: int = 0) -> None:
        """Herd branch initial

        :param str url: URL of repo
        :param str branch: Branch name to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch)
        if not self.existing_remote_branch(branch, self.remote):
            remote_output = fmt.remote_string(self.remote)
            self._print(f' - No existing remote branch {remote_output} {fmt.ref_string(branch)}')
            self._herd_initial(url, depth=depth)
            return
        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _herd_existing_local(self, remote: str, branch: str, depth: int = 0, rebase: bool = False) -> None:
        """Herd ref

        :param str remote: Remote name
        :param str branch: Git branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        self._checkout_branch(branch)

        if not self.existing_remote_branch(branch, remote):
            return

        if not self._is_tracking_branch(branch):
            self._set_tracking_branch_commit(branch, remote, depth)
            return

        if rebase:
            self._rebase_remote_branch(remote, branch)
            return

        self._pull(remote, branch)

    def _herd_initial(self, url: str, depth: int = 0) -> None:
        """Herd ref initial

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if ref_type(self.default_ref) == 'branch':
            self._checkout_new_repo_branch(truncate_ref(self.default_ref), depth)
        elif ref_type(self.default_ref) == 'tag':
            self._checkout_new_repo_tag(truncate_ref(self.default_ref), self.remote, depth, remove_dir=True)
        elif ref_type(self.default_ref) == 'sha':
            self._checkout_new_repo_commit(self.default_ref, self.remote, depth)

    def _herd_remote_branch(self, remote: str, branch: str, depth: int = 0, rebase: bool = False) -> None:
        """Herd remote branch

        :param str remote: Remote name
        :param str branch: Branch name to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        if not self._is_tracking_branch(branch):
            self._set_tracking_branch_commit(branch, remote, depth)
            return

        if rebase:
            self._rebase_remote_branch(remote, branch)
            return

        self._pull(remote, branch)
