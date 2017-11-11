# -*- coding: utf-8 -*-
"""Project Git utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from git import GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_git_error import ClowderGitError
from clowder.git.project_repo_impl import ProjectRepoImpl
from clowder.git.util import (
    existing_git_repository,
    ref_type,
    truncate_ref
)
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command

__project_repo_default_ref__ = 'refs/heads/master'
__project_repo_default_remote__ = 'origin'


class ProjectRepo(ProjectRepoImpl):
    """Class encapsulating git utilities for projects

    :ivar str repo_path: Absolute path to repo
    :ivar str default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar bool parallel: Whether command is being run in parallel, affects output
    :ivar Repo repo: Repo instance
    """

    def __init__(self, repo_path, remote, default_ref, parallel=False):
        """ProjectRepo __init__

        :param str repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        """

        ProjectRepoImpl.__init__(self, repo_path, remote, default_ref, parallel=parallel)

    def create_clowder_repo(self, url, branch, depth=0):
        """Clone clowder git repo from url at path

        .. py:function:: create_clowder_repo(url, branch, depth=0)

        :param str url: URL of repo
        :param str branch: Branch name
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        if existing_git_repository(self.repo_path):
            return

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url):
        """Configure remotes names for fork and upstream

        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        :param str fork_remote_name: Fork remote name
        :param str fork_remote_url: Fork remote url
        """

        if not existing_git_repository(self.repo_path):
            return

        try:
            remotes = self.repo.remotes
        except GitError:
            return
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            for remote in remotes:
                if upstream_remote_url == self._remote_get_url(remote.name) and remote.name != upstream_remote_name:
                    self._rename_remote(remote.name, upstream_remote_name)
                    continue
                if fork_remote_url == self._remote_get_url(remote.name) and remote.name != fork_remote_name:
                    self._rename_remote(remote.name, fork_remote_name)
            self._compare_remotes(upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url)

    def herd(self, url, **kwargs):
        """Herd ref

        .. py:function:: herd(url, depth=0, fetch=True, rebase=False)

        :param str url: URL of repo

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            fetch (bool): Whether to fetch
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        fetch = kwargs.get('fetch', True)
        rebase = kwargs.get('rebase', False)

        if not existing_git_repository(self.repo_path):
            self._herd_initial(url, depth=depth)
            return

        self._create_remote(self.remote, url)
        self._herd(self.remote, self.default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_branch(self, url, branch, **kwargs):
        """Herd branch

        .. py:function:: herd_branch(url, branch, depth=0, fork_remote=None, rebase=False)

        :param str url: URL of repo
        :param str branch: Branch name

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            fork_remote (str): Fork remote name
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        rebase = kwargs.get('rebase', False)
        fork_remote = kwargs.get('fork_remote', None)

        if not existing_git_repository(self.repo_path):
            self._herd_branch_initial(url, branch, depth=depth)
            return

        branch_output = fmt.ref_string(branch)
        branch_ref = 'refs/heads/' + branch
        if self.existing_local_branch(branch):
            self._herd_branch_existing_local(branch, depth=depth, rebase=rebase, fork_remote=fork_remote)
            return

        self.fetch(self.remote, depth=depth, ref=branch_ref, allow_failure=True)
        if self.existing_remote_branch(branch, self.remote):
            self._herd(self.remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return

        remote_output = fmt.remote_string(self.remote)
        self._print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd(fork_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return

            remote_output = fmt.remote_string(fork_remote)
            self._print(' - No existing remote branch ' + remote_output + ' ' + branch_output)

        fetch = depth != 0
        self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_tag(self, url, tag, **kwargs):
        """Herd tag

        .. py:function:: herd_tag(url, tag, depth=0, rebase=False)

        :param str url: URL of repo
        :param str tag: Tag name

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        rebase = kwargs.get('rebase', False)

        if not existing_git_repository(self.repo_path):
            self._init_repo()
            self._create_remote(self.remote, url, remove_dir=True)
            try:
                self._checkout_new_repo_tag(tag, self.remote, depth)
            except ClowderGitError:
                fetch = depth != 0
                self.herd(url, depth=depth, fetch=fetch, rebase=rebase)
                return

        try:
            self.fetch(self.remote, ref='refs/tags/' + tag, depth=depth)
            self._checkout_tag(tag)
        except ClowderGitError:
            fetch = depth != 0
            self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_remote(self, url, remote, branch=None):
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
        except ClowderGitError:
            self.fetch(remote, ref=self.default_ref)

    def prune_branch_local(self, branch, force):
        """Prune local branch

        :param str branch: Branch name to delete
        :param bool force: Force delete branch
        """

        branch_output = fmt.ref_string(branch)
        if branch not in self.repo.heads:
            self._print(' - Local branch ' + branch_output + " doesn't exist")
            return

        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            ref_output = fmt.ref_string(truncate_ref(self.default_ref))
            try:
                self._print(' - Checkout ref ' + ref_output)
                self.repo.git.checkout(truncate_ref(self.default_ref))
            except GitError as err:
                message = colored(' - Failed to checkout ref', 'red') + ref_output
                self._print(message)
                self._print(fmt.error(err))
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit()

        try:
            self._print(' - Delete local branch ' + branch_output)
            self.repo.delete_head(branch, force=force)
        except GitError as err:
            message = colored(' - Failed to delete local branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def prune_branch_remote(self, branch, remote):
        """Prune remote branch in repository

        :param str branch: Branch name to delete
        :param str remote: Remote name
        """

        branch_output = fmt.ref_string(branch)
        if not self.existing_remote_branch(branch, remote):
            self._print(' - Remote branch ' + branch_output + " doesn't exist")
            return

        try:
            self._print(' - Delete remote branch ' + branch_output)
            self.repo.git.push(remote, '--delete', branch)
        except GitError as err:
            message = colored(' - Failed to delete remote branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def reset(self, depth=0):
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        .. py:function:: reset(depth=0)

        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
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
            message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._exit(message)

        self.fetch(self.remote, ref=self.default_ref, depth=depth)
        self._print(' - Reset branch ' + branch_output + ' to ' + remote_output + ' ' + branch_output)
        remote_branch = self.remote + '/' + branch
        self._reset_head(branch=remote_branch)

    def reset_timestamp(self, timestamp, author, ref):
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        """

        rev = None
        if author:
            rev = self._find_rev_by_timestamp_author(timestamp, author, ref)
        if not rev:
            rev = self._find_rev_by_timestamp(timestamp, ref)
        if not rev:
            message = colored(' - Failed to find rev', 'red')
            self._print(message)
            self._exit(message)

        self._checkout_sha(rev)

    def start(self, remote, branch, depth, tracking):
        """Start new branch in repository

        :param str remote: Remote name
        :param str branch: Local branch name to create
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        if branch not in self.repo.heads:
            if not is_offline():
                self.fetch(remote, ref=branch, depth=depth)
            try:
                self._create_branch_local(branch)
                self._checkout_branch_local(branch)
            except ClowderGitError:
                self._exit()
        else:
            print(' - ' + fmt.ref_string(branch) + ' already exists')
            if self._is_branch_checked_out(branch):
                print(' - On correct branch')
            else:
                try:
                    self._checkout_branch_local(branch)
                except ClowderGitError:
                    self._exit()

        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote

        .. py:function:: sync(fork_remote, rebase=False)

        :param str fork_remote: Fork remote name
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes.
        """

        self._print(' - Sync fork with upstream remote')
        if ref_type(self.default_ref) != 'branch':
            message = colored(' - Can only sync branches', 'red')
            self._print(message)
            self._exit(message)

        fork_remote_output = fmt.remote_string(fork_remote)
        branch_output = fmt.ref_string(truncate_ref(self.default_ref))
        if rebase:
            self._rebase_remote_branch(self.remote, truncate_ref(self.default_ref))
        else:
            self._pull(self.remote, truncate_ref(self.default_ref))

        self._print(' - Push to ' + fork_remote_output + ' ' + branch_output)
        command = ['git', 'push', fork_remote, truncate_ref(self.default_ref)]
        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError:
            message = colored(' - Failed to push to ', 'red') + fork_remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _compare_remotes(self, upstream_remote_name, upstream_remote_url, fork_remote_name, fork_remote_url):
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

    def _herd(self, remote, ref, **kwargs):
        """Herd ref

        .. py:function:: _herd(remote, ref, depth=0, fetch=True, rebase=False)

        :param str remote: Remote name
        :param str ref: Git ref

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            fetch (bool): Whether to fetch
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        fetch = kwargs.get('fetch', True)
        rebase = kwargs.get('rebase', False)

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

    def _herd_branch_existing_local(self, branch, **kwargs):
        """Herd branch for existing local branch

        .. py:function:: herd_branch_existing_local(branch, depth=0, fork_remote=None, rebase=False)

        :param str branch: Branch name

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            fork_remote (str): Fork remote name
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        rebase = kwargs.get('rebase', False)
        fork_remote = kwargs.get('fork_remote', None)

        self._checkout_branch(branch)

        branch_ref = 'refs/heads/' + branch
        self.fetch(self.remote, depth=depth, ref=branch_ref)
        if self.existing_remote_branch(branch, self.remote):
            self._herd_remote_branch(self.remote, branch, depth=depth, rebase=rebase)
            return

        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd_remote_branch(fork_remote, branch, depth=depth, rebase=rebase)

    def _herd_branch_initial(self, url, branch, depth=0):
        """Herd branch initial

        .. py:function:: _herd_branch_initial(url, branch, depth=0)

        :param str url: URL of repo
        :param str branch: Branch name to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch)
        if not self.existing_remote_branch(branch, self.remote):
            remote_output = fmt.remote_string(self.remote)
            self._print(' - No existing remote branch ' + remote_output + ' ' + fmt.ref_string(branch))
            self._herd_initial(url, depth=depth)
            return
        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _herd_existing_local(self, remote, branch, **kwargs):
        """Herd ref

        .. py:function:: _herd_existing_local(remote, ref, depth=0, fetch=True, rebase=False)

        :param str remote: Remote name
        :param str branch: Git branch name

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        rebase = kwargs.get('rebase', False)

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

    def _herd_initial(self, url, depth=0):
        """Herd ref initial

        .. py:function:: _herd_initial(url, depth=0)

        :param str url: URL of repo
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if ref_type(self.default_ref) == 'branch':
            self._checkout_new_repo_branch(truncate_ref(self.default_ref), depth)
        elif ref_type(self.default_ref) == 'tag':
            self._checkout_new_repo_tag(truncate_ref(self.default_ref), self.remote, depth, remove_dir=True)
        elif ref_type(self.default_ref) == 'sha':
            self._checkout_new_repo_commit(self.default_ref, self.remote, depth)

    def _herd_remote_branch(self, remote, branch, **kwargs):
        """Herd remote branch

        .. py:function:: _herd_remote_branch(remote, branch, depth=0, rebase=False)

        :param str remote: Remote name
        :param str branch: Branch name to attempt to herd

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
        """

        depth = kwargs.get('depth', 0)
        rebase = kwargs.get('rebase', False)

        if not self._is_tracking_branch(branch):
            self._set_tracking_branch_commit(branch, remote, depth)
            return

        if rebase:
            self._rebase_remote_branch(remote, branch)
            return

        self._pull(remote, branch)
