# -*- coding: utf-8 -*-
"""Project Git abstract utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from git import Repo, GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_git_error import ClowderGitError
from clowder.git.repo import GitRepo
from clowder.git.util import (
    existing_git_repository,
    not_detached
)
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory

__project_repo_default_ref__ = 'refs/heads/master'
__project_repo_default_remote__ = 'origin'


class ProjectRepoImpl(GitRepo):
    """Abstract class encapsulating private git utilities for projects

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

    def _checkout_branch(self, branch):
        """Checkout local branch or print message if already checked out

        .. py:function:: _checkout_branch(branch)

        :param str branch: Branch name
        """

        if self._is_branch_checked_out(branch):
            self._print(' - Branch ' + fmt.ref_string(branch) + ' already checked out')
        else:
            self._checkout_branch_local(branch)

    def _checkout_branch_local(self, branch, remove_dir=False):
        """Checkout local branch

        .. py:function:: _checkout_branch_local(branch, remove_dir=False)

        :param str branch: Branch name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Checkout branch ' + branch_output)
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
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

        .. py:function:: _checkout_new_repo_tag(tag, remote, depth, remove_dir=False)

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
        """

        remote_tag = self._get_remote_tag(tag, remote, depth=depth, remove_dir=remove_dir)
        if remote_tag is None:
            return 1

        tag_output = fmt.ref_string(tag)
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
            raise ClowderGitError(msg=' - No existing tag ' + tag_output)

        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                self._print(' - On correct commit for tag')
                return
            self._print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout('refs/tags/' + tag)
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
        :raise ClowderGitError:
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(' - Create branch ' + branch_output)
            self.repo.create_head(branch)
        except GitError as err:
            message = colored(' - Failed to create branch ', 'red')
            self._print(message + branch_output)
            self._print(fmt.error(err))
            raise ClowderGitError(err)
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
            self.fetch(remote, depth=depth, ref=branch, remove_dir=remove_dir)

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
            self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch, remote, depth):
        """Create remote tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        branch_output = fmt.ref_string(branch)
        self.fetch(remote, depth=depth, ref=branch)

        if branch in self._remote(remote).refs:
            self._print_existing_remote_branch_message(branch)
            return

        try:
            self._print(' - Push remote branch ' + branch_output)
            self.repo.git.push(remote, branch)
            self._set_tracking_branch(remote, branch)
        except GitError as err:
            message = colored(' - Failed to push remote branch ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _create_remote(self, remote, url, remove_dir=False):
        """Create new remote

        .. py:function:: _create_remote(remote, url, remove_dir=False)

        :param str remote: Remote name
        :param str url: URL of repo
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
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

    def _get_remote_tag(self, tag, remote, depth=0, remove_dir=False):
        """Returns Tag object

        .. py:function:: _get_remote_tag(tag, remote, depth=0, remove_dir=False)

        :param str tag: Tag name
        :param str remote: Remote name
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
        :return: GitPython Tag object if it exists, otherwise None
        :rtype: Tag
        """

        tag_output = fmt.ref_string(tag)
        self._remote(remote, remove_dir=remove_dir)
        self.fetch(remote, depth=depth, ref='refs/tags/' + tag, remove_dir=remove_dir)

        try:
            return self.repo.tags[tag]
        except (GitError, IndexError):
            message = ' - No existing tag '
            if remove_dir:
                remove_directory(self.repo_path)
                self._print(colored(message, 'red') + tag_output)
                self._exit(fmt.parallel_exception_error(self.repo_path, colored(message, 'red'), tag_output))
            if self._print_output:
                self._print(message + tag_output)
            return None
        except (KeyboardInterrupt, SystemExit):
            if remove_dir:
                remove_directory(self.repo_path)
            self._exit()

    def _init_repo(self):
        """Initialize repository

        :raise OSError:
        """

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

    def _print_existing_remote_branch_message(self, branch):
        """Print output message for existing remote branch

        :param str branch: Branch name
        """

        branch_output = fmt.ref_string(branch)
        try:
            self.repo.git.config('--get', 'branch.' + branch + '.merge')
        except GitError:
            message = colored(' - Remote branch ', 'red') + branch_output + colored(' already exists\n', 'red')
            self._print(message)
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            self._print(' - Tracking branch ' + branch_output + ' already exists')

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

        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError:
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

        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError:
            message = colored(' - Failed to rebase onto ', 'red') + remote_output + ' ' + branch_output
            self._print(message)
            self._print(fmt.command_failed_error(command))
            self._exit(message)

    def _remote(self, remote, remove_dir=False):
        """Get GitPython Remote instance

        .. py:function:: _remote(remote, remove_dir=False)

        :param str remote: Remote name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
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

        .. py:function:: _set_tracking_branch(remote, branch, remove_dir=False)

        :param str remote: Remote name
        :param str branch: Branch name
        :param Optional[bool] remove_dir: Whether to remove the directory if commands fail
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            self._print(' - Set tracking branch ' + branch_output + ' -> ' + remote_output + ' ' + branch_output)
            local_branch.set_tracking_branch(remote_branch)
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
        self.fetch(remote, depth=depth, ref=branch)

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

        self._set_tracking_branch(remote, branch)
