# -*- coding: utf-8 -*-
"""Project Git utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

from git import Repo, GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_git_error import ClowderGitError
from clowder.git.repo import execute_command, GitRepo
from clowder.git.util import (
    existing_git_repository,
    not_detached,
    ref_type,
    truncate_ref
)
from clowder.util.connectivity import is_offline
from clowder.util.file_system import remove_directory

__project_repo_default_ref__ = 'refs/heads/master'
__project_repo_default_remote__ = 'origin'


class ProjectRepo(GitRepo):
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

        GitRepo.__init__(self, repo_path, remote, default_ref, parallel=parallel)

    def create_clowder_repo(self, url, branch, depth=0):
        """Clone clowder git repo from url at path

        :param str url: URL of repo
        :param str branch: Branch name
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            Defaults to 0
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
                if upstream_remote_url == self._remote_get_url(remote.name):
                    if remote.name != upstream_remote_name:
                        self._rename_remote(remote.name, upstream_remote_name)
                        continue
                if fork_remote_url == self._remote_get_url(remote.name):
                    if remote.name != fork_remote_name:
                        self._rename_remote(remote.name, fork_remote_name)
            remote_names = [r.name for r in self.repo.remotes]
            if upstream_remote_name in remote_names:
                self._compare_remote_url(upstream_remote_name, upstream_remote_url)
            if fork_remote_name in remote_names:
                self._compare_remote_url(fork_remote_name, fork_remote_url)

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
        return_code = self._create_remote(self.remote, url)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to create remote', 'red'))
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
            if self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            self.fetch(self.remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, self.remote):
                self._herd_remote_branch(self.remote, branch, depth=depth, rebase=rebase)
                return
            if fork_remote:
                self.fetch(fork_remote, depth=depth, ref=branch_ref)
                if self.existing_remote_branch(branch, fork_remote):
                    self._herd_remote_branch(fork_remote, branch, depth=depth, rebase=rebase)
            return
        self.fetch(self.remote, depth=depth, ref=branch_ref)
        if self.existing_remote_branch(branch, self.remote):
            self._herd(self.remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return
        else:
            remote_output = fmt.remote_string(self.remote)
            self._print(' - No existing remote branch ' + remote_output + ' ' + branch_output)
        if fork_remote:
            self.fetch(fork_remote, depth=depth, ref=branch_ref)
            if self.existing_remote_branch(branch, fork_remote):
                self._herd(fork_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return
            else:
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
            return_code = self._checkout_new_repo_tag(tag, self.remote, depth)
            if return_code == 0:
                return
            fetch = depth != 0
            self.herd(url, depth=depth, fetch=fetch, rebase=rebase)
            return
        return_code = self.fetch(self.remote, ref='refs/tags/' + tag, depth=depth)
        if return_code == 0:
            return_code = self._checkout_tag(tag)
            if return_code == 0:
                return
        fetch = depth != 0
        self.herd(url, depth=depth, fetch=fetch, rebase=rebase)

    def herd_remote(self, url, remote, branch=None):
        """Herd remote repo

        :param str url: URL of repo
        :param str remote: Remote name
        :param Optional[str] branch: Branch name
        """

        return_code = self._create_remote(remote, url)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to create remote', 'red'))
        if branch:
            return_code = self.fetch(remote, ref=branch)
            if return_code == 0:
                return
        return_code = self.fetch(remote, ref=self.default_ref)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to fetch', 'red'))

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
            return
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

        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer.
            Defaults to 0
        """

        if ref_type(self.default_ref) == 'branch':
            branch = truncate_ref(self.default_ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=True)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red') + branch_output
                    self._print(message)
                    self._exit(message)
                return
            elif self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            remote_output = fmt.remote_string(self.remote)
            if not self.existing_remote_branch(branch, self.remote):
                message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
                self._print(message)
                self._exit(message)
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._print(' - Reset branch ' + branch_output + ' to ' + remote_output + ' ' + branch_output)
            remote_branch = self.remote + '/' + branch
            self._reset_head(branch=remote_branch)
        elif ref_type(self.default_ref) == 'tag':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_tag(truncate_ref(self.default_ref))
        elif ref_type(self.default_ref) == 'sha':
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_sha(self.default_ref)

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
                return_code = self.fetch(remote, ref=branch, depth=depth)
                if return_code != 0:
                    sys.exit(1)
            return_code = self._create_branch_local(branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
            return_code = self._checkout_branch_local(branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
        else:
            branch_output = fmt.ref_string(branch)
            print(' - ' + branch_output + ' already exists')
            correct_branch = self._is_branch_checked_out(branch)
            if correct_branch:
                print(' - On correct branch')
            else:
                return_code = self._checkout_branch_local(branch)
                if return_code != 0:
                    self._exit('', return_code=return_code)
        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote

        :param str fork_remote: Fork remote name
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
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
        return_code = execute_command(command, self.repo_path, print_output=self._print_output)
        if return_code != 0:
            message = colored(' - Failed to push to ', 'red') + fork_remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _checkout_branch_local(self, branch, remove_dir=False):
        """Checkout local branch

        :param str branch: Branch name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail. Defaults to False
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Checkout branch ' + branch_output)
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
            return 0
        except GitError as err:
            if remove_dir:
                remove_directory(self.repo_path)
            message = colored(' - Failed to checkout branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, branch_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()

    def _checkout_new_repo_branch(self, branch, depth):
        """Checkout remote branch or fail and delete repo if it doesn't exist

        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(self.remote)
        self._remote(self.remote, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch, remove_dir=True)

        if not self.existing_remote_branch(branch, self.remote):
            remove_directory(self.repo_path)
            message = colored(' - No existing remote branch ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._exit(fmt.parallel_exception_error(self.repo_path, message))

        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _checkout_new_repo_commit(self, commit, remote, depth):
        """Checkout commit or fail and delete repo if it doesn't exist

        :param str commit: Commit sha
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        commit_output = fmt.ref_string(commit)
        self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=commit, remove_dir=True)

        self._print(' - Checkout commit ' + commit_output)
        try:
            self.repo.git.checkout(commit)
        except GitError as err:
            remove_directory(self.repo_path)
            message = colored(' - Failed to checkout commit ', 'red')
            self._print(message + commit_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, commit_output))
        except (KeyboardInterrupt, SystemExit):
            remove_directory(self.repo_path)
            self._exit()

    def _checkout_new_repo_tag(self, tag, remote, depth, remove_dir=False):
        """Checkout tag or fail and delete repo if it doesn't exist

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail. Defaults to False
        """

        tag_output = fmt.ref_string(tag)
        self._remote(remote, remove_dir=remove_dir)
        self.fetch(remote, depth=depth, ref='refs/tags/' + tag, remove_dir=remove_dir)

        try:
            remote_tag = self.repo.tags[tag]
        except (GitError, IndexError):
            message = ' - No existing tag '
            if remove_dir:
                remove_directory(self.repo_path)
                self._print(colored(message, 'red') + tag_output)
                self._exit(fmt.parallel_exception_error(self.repo_path, colored(message, 'red'), tag_output))
            if self._print_output:
                self._print(message + tag_output)
            return 1
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()
        else:
            try:
                self._print(' - Checkout tag ' + tag_output)
                self.repo.git.checkout(remote_tag)
                return 0
            except GitError as err:
                message = colored(' - Failed to checkout tag ', 'red')
                self._print(message + tag_output)
                self._print(fmt.error(err))
                if remove_dir:
                    remove_directory(self.repo_path)
                    self._exit(fmt.parallel_exception_error(self.repo_path, message, tag_output))
                return 1
            except (KeyboardInterrupt, SystemExit):
                if remove_dir:
                    remove_directory(self.repo_path)
                self._exit()

    def _checkout_sha(self, sha):
        """Checkout commit by sha

        :param str sha: Commit sha
        """

        commit_output = fmt.ref_string(sha)
        try:
            if self.repo.head.commit.hexsha == sha:
                self._print(' - On correct commit')
                return 0
            self._print(' - Checkout commit ' + commit_output)
            self.repo.git.checkout(sha)
        except GitError as err:
            message = colored(' - Failed to checkout commit ', 'red')
            self._print(message + commit_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, commit_output))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _checkout_tag(self, tag):
        """Checkout commit tag is pointing to

        :param str tag: Tag name
        """

        tag_output = fmt.ref_string(tag)
        if tag not in self.repo.tags:
            self._print(' - No existing tag ' + tag_output)
            return 1

        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                self._print(' - On correct commit for tag')
                return 0
            self._print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout('refs/tags/' + tag)
            return 0
        except (GitError, ValueError) as err:
            message = colored(' - Failed to checkout tag ', 'red')
            self._print(message + tag_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, tag_output))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _compare_remote_url(self, remote, url):
        """Compare actual remote url to given url

        If URL's are different print error message and exit

        :param str remote: Remote name
        :param str url: URL to compare with remote's URL
        """

        if url != self._remote_get_url(remote):
            actual_url = self._remote_get_url(remote)
            message = fmt.remote_already_exists_error(remote, url, actual_url)
            self._print(message)
            self._exit(message)

    def _create_branch_local(self, branch):
        """Create local branch

        :param str branch: Branch name
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Create branch ' + branch_output)
            self.repo.create_head(branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to create branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            return 1
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _create_branch_local_tracking(self, branch, remote, depth, **kwargs):
        """Create and checkout tracking branch

        .. py:function:: _create_branch_local_tracking(self, branch, remote, depth, fetch=True, remove_dir=False)

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer

        Keyword Args:
            fetch (bool): Whether to fetch before creating branch
            remove_dir (bool): Whether to remove the directory if commands fail
        """

        fetch = kwargs.get('fetch', True)
        remove_dir = kwargs.get('remove_dir', False)

        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote, remove_dir=remove_dir)
        if fetch:
            return_code = self.fetch(remote, depth=depth, ref=branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code

        try:
            self._print(' - Create branch ' + branch_output)
            self.repo.create_head(branch, origin.refs[branch])
        except (GitError, IndexError) as err:
            message = colored(' - Failed to create branch ', 'red') + branch_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()
        else:
            return_code = self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            if return_code != 0:
                return return_code
            return self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch, remote, depth):
        """Create remote tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        return_code = self.fetch(remote, depth=depth, ref=branch)

        if return_code != 0:
            self._exit('', return_code=return_code)

        if branch in origin.refs:
            try:
                self.repo.git.config('--get', 'branch.' + branch + '.merge')
                self._print(' - Tracking branch ' + branch_output + ' already exists')
                return
            except GitError:
                message_1 = colored(' - Remote branch ', 'red')
                message_2 = colored(' already exists', 'red')
                message = message_1 + branch_output + message_2 + '\n'
                self._print(message)
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit()

        try:
            self._print(' - Push remote branch ' + branch_output)
            self.repo.git.push(remote, branch)
            return_code = self._set_tracking_branch(remote, branch)
            if return_code != 0:
                self._exit('', return_code=return_code)
        except GitError as err:
            message = colored(' - Failed to push remote branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _create_remote(self, remote, url, remove_dir=False):
        """Create new remote

        :param str remote: Remote name
        :param str url: URL of repo
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail. Defaults to False
        """

        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return 0

        remote_output = fmt.remote_string(remote)
        try:
            self._print(' - Create remote ' + remote_output)
            self.repo.create_remote(remote, url)
            return 0
        except GitError as err:
            message = colored(' - Failed to create remote ', 'red')
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message + remote_output)
            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, remote_output))
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()

    def _find_rev_by_timestamp(self, timestamp, ref):
        """Find rev by timestamp

        :param str timestamp: Commit ref timestamp
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp
        :rtype: str
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, ref)
        except GitError as err:
            message = colored(' - Failed to find rev from timestamp', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _find_rev_by_timestamp_author(self, timestamp, author, ref):
        """Find rev by timestamp and author

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp by author
        :rtype: str
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, '--author', author, ref)
        except GitError as err:
            message = colored(' - Failed to find rev from timestamp by author', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

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

        if ref_type(ref) == 'branch':
            branch = truncate_ref(ref)
            branch_output = fmt.ref_string(branch)
            if not self.existing_local_branch(branch):
                return_code = self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                if return_code != 0:
                    message = colored(' - Failed to create tracking branch ', 'red') + branch_output
                    self._print(message)
                    self._exit(message)
                return
            elif self._is_branch_checked_out(branch):
                self._print(' - Branch ' + branch_output + ' already checked out')
            else:
                self._checkout_branch_local(branch)
            if not self.existing_remote_branch(branch, remote):
                return
            if not self._is_tracking_branch(branch):
                self._set_tracking_branch_commit(branch, remote, depth)
                return
            if rebase:
                self._rebase_remote_branch(remote, branch)
                return
            self._pull(remote, branch)
        elif ref_type(ref) == 'tag':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(truncate_ref(ref))
        elif ref_type(ref) == 'sha':
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref)

    def _herd_initial(self, url, depth=0):
        """Herd ref initial

        :param str url: URL of repo
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer.
            Defaults to 0
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if ref_type(self.default_ref) == 'branch':
            self._checkout_new_repo_branch(truncate_ref(self.default_ref), depth)
        elif ref_type(self.default_ref) == 'tag':
            self._checkout_new_repo_tag(truncate_ref(self.default_ref), self.remote, depth, remove_dir=True)
        elif ref_type(self.default_ref) == 'sha':
            self._checkout_new_repo_commit(self.default_ref, self.remote, depth)

    def _herd_branch_initial(self, url, branch, depth=0):
        """Herd branch initial

        :param str url: URL of repo
        :param str branch: Branch name to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer.
            Defaults to 0
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

    def _init_repo(self):
        """Initialize repository"""

        if existing_git_repository(self.repo_path):
            return

        try:
            self._print(' - Initialize repo at ' + fmt.get_path(self.repo_path))
            if not os.path.isdir(self.repo_path):
                try:
                    os.makedirs(self.repo_path)
                except OSError as err:
                    if err.errno != os.errno.EEXIST:
                        raise
            self.repo = Repo.init(self.repo_path)
        except GitError as err:
            remove_directory(self.repo_path)
            message = colored(' - Failed to initialize repository', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            remove_directory(self.repo_path)
            self._exit()

    def _is_branch_checked_out(self, branch):
        """Check if branch is checked out

        :param str branch: Branch name
        :return: True, if branch is checked out
        :rtype: bool
        """

        try:
            default_branch = self.repo.heads[branch]
            is_detached = self.repo.head.is_detached
            same_branch = self.repo.head.ref == default_branch
            return not is_detached and same_branch
        except (GitError, TypeError):
            return False
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _is_tracking_branch(self, branch):
        """Check if branch is a tracking branch

        :param str branch: Branch name
        :return: True, if branch has a tracking relationship
        :rtype: bool
        """

        branch_output = fmt.ref_string(branch)
        try:
            local_branch = self.repo.heads[branch]
            tracking_branch = local_branch.tracking_branch()
            return True if tracking_branch else False
        except GitError as err:
            message = colored(' - No existing branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    @not_detached
    def _pull(self, remote, branch):
        """Pull from remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Pull from ' + remote_output + ' ' + branch_output)
        command = ['git pull', remote, branch]

        return_code = execute_command(command, self.repo_path, print_output=self._print_output)
        if return_code != 0:
            message = colored(' - Failed to pull from ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._exit(message)

    @not_detached
    def _rebase_remote_branch(self, remote, branch):
        """Rebase onto remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(' - Rebase onto ' + remote_output + ' ' + branch_output)
        command = ['git pull --rebase', remote, branch]

        return_code = execute_command(command, self.repo_path, print_output=self._print_output)
        if return_code != 0:
            message = colored(' - Failed to rebase onto ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _remote(self, remote, remove_dir=False):
        """Get GitPython Remote instance

        :param str remote: Remote name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail. Defaults to False
        :return: GitPython Remote instance
        :rtype: Remote
        """

        remote_output = fmt.remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            message = colored(' - No existing remote ', 'red') + remote_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _remote_get_url(self, remote):
        """Get url of remote

        :param str remote: Remote name
        :return: URL of remote
        :rtype: str
        """

        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from, remote_to):
        """Rename remote

        :param str remote_from: Name of remote to rename
        :param str remote_to: Name to rename remote to
        """

        remote_output_f = fmt.remote_string(remote_from)
        remote_output_t = fmt.remote_string(remote_to)
        self._print(' - Rename remote ' + remote_output_f + ' to ' + remote_output_t)
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            message = colored(' - Failed to rename remote from ', 'red') + remote_output_f + ' to ' + remote_output_t
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _set_tracking_branch(self, remote, branch, remove_dir=False):
        """Set tracking branch

        :param str remote: Remote name
        :param str branch: Branch name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail. Defaults to False
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            self._print(' - Set tracking branch ' + branch_output + ' -> ' + remote_output + ' ' + branch_output)
            local_branch.set_tracking_branch(remote_branch)
            return 0
        except GitError as err:
            message = colored(' - Failed to set tracking branch ', 'red') + branch_output
            if remove_dir:
                remove_directory(self.repo_path)
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()

    def _set_tracking_branch_commit(self, branch, remote, depth):
        """Set tracking relationship between local and remote branch if on same commit

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        return_code = self.fetch(remote, depth=depth, ref=branch)
        if return_code != 0:
            raise ClowderGitError(msg=colored(' - Failed to fech', 'red'))
        if not self.existing_local_branch(branch):
            message = colored(' - No local branch ', 'red') + branch_output + '\n'
            self._print(message)
            self._exit(message)
        if not self.existing_remote_branch(branch, remote):
            message = colored(' - No remote branch ', 'red') + branch_output + '\n'
            self._print(message)
            self._exit(message)
        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message_1 = colored(' - Existing remote branch ', 'red')
            message_2 = colored(' on different commit', 'red')
            message = message_1 + branch_output + message_2 + '\n'
            self._print(message)
            self._exit(message_1)
        return_code = self._set_tracking_branch(remote, branch)
        if return_code != 0:
            self._exit(colored(' - Failed to set tracking branch', 'red'))
