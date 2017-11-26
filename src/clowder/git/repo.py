# -*- coding: utf-8 -*-
"""Base Git utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import subprocess

from git import Repo, GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_git_error import ClowderGitError
from clowder.git.util import (
    existing_git_repository,
    not_detached,
    truncate_ref,
)
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory

__repo_default_ref__ = 'refs/heads/master'
__repo_default_remote__ = 'origin'


class GitRepo(object):
    """Class encapsulating base git utilities

    :ivar str repo_path: Absolute path to repo
    :ivar str default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar bool parallel: Whether command is being run in parallel, affects output
    :ivar Repo repo: Repo instance
    """

    def __init__(self, repo_path, remote, default_ref, parallel=False):
        """GitRepo __init__

        :param str repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param str default_ref: Default ref
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        """

        self.repo_path = repo_path
        self.default_ref = default_ref
        self.remote = remote
        self.parallel = parallel
        self.repo = self._repo() if existing_git_repository(repo_path) else None
        self._print_output = not parallel

    def add(self, files):
        """Add files to git index

        :param str files: Files to git add
        """

        self._print(' - Add files to git index')
        try:
            print(self.repo.git.add(files))
        except GitError as err:
            message = colored(' - Failed to add files to git index\n', 'red') + fmt.error(err)
            self._print(message)
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            self.status_verbose()

    def checkout(self, truncated_ref, allow_failure=False):
        """Checkout git ref

        .. py:function:: checkout(truncated_ref, allow_failure=False)

        :param str truncated_ref: Ref to git checkout
        :param Optional[bool] allow_failure: Whether to allow failing to checkout branch
        """

        ref_output = fmt.ref_string(truncated_ref)
        try:
            self._print(' - Check out ' + ref_output)
            if self._print_output:
                print(self.repo.git.checkout(truncated_ref))
                return

            self.repo.git.checkout(truncated_ref)
        except GitError as err:
            message = colored(' - Failed to checkout ', 'red')
            self._print(message + ref_output)
            if allow_failure:
                return

            self._print(fmt.error(err))
            self._exit(fmt.parallel_exception_error(self.repo_path, message, ref_output))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def clean(self, args=''):
        """Discard changes for repo

        :param Optional[str] args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        """

        self._print(' - Clean project')
        clean_args = '-f' if args == '' else '-f' + args
        self._clean(args=clean_args)
        self._print(' - Reset project')
        self._reset_head()
        if self._is_rebase_in_progress():
            self._print(' - Abort rebase in progress')
            self._abort_rebase()

    def commit(self, message):
        """Commit current changes

        :param str message: Git commit message
        """

        try:
            self._print(' - Commit current changes')
            print(self.repo.git.commit(message=message))
        except GitError as err:
            message = colored(' - Failed to commit current changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def current_branch(self):
        """Return currently checked out branch of project

        :return: Name of currently checked out branch
        :rtype: str
        """

        return self.repo.head.ref.name

    def existing_remote_branch(self, branch, remote):
        """Check if remote branch exists

        :param str branch: Branch name
        :param str remote: Remote name
        :return: True, if remote branch exists
        :rtype: bool
        """

        try:
            origin = self.repo.remotes[remote]
            return branch in origin.refs
        except (GitError, IndexError):
            return False
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def existing_local_branch(self, branch):
        """Check if local branch exists

        :param str branch: Branch name
        :return: True, if local branch exists
        :rtype: bool
        """

        return branch in self.repo.heads

    def fetch(self, remote, **kwargs):
        """Fetch from a specific remote ref

        .. py:function:: fetch(remote, ref=None, depth=0, remove_dir=False, allow_failure=False)

        :param str remote: Remote name

        Keyword Args:
            ref (str): Ref to fetch
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            remove_dir (bool): Whether to remove the directory if commands fail
            allow_failure (bool): Whether to allow failure
        """

        ref = kwargs.get('ref', None)
        depth = kwargs.get('depth', 0)
        remove_dir = kwargs.get('remove_dir', False)
        allow_failure = kwargs.get('allow_failure', False)

        remote_output = fmt.remote_string(remote)
        if depth == 0:
            self._print(' - Fetch from ' + remote_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output
            command = ['git fetch', remote, '--prune --tags']
        elif ref is None:
            command = ['git fetch', remote, '--depth', str(depth), '--prune --tags']
            message = colored(' - Failed to fetch remote ', 'red')
            error = message + remote_output
        else:
            ref_output = fmt.ref_string(truncate_ref(ref))
            self._print(' - Fetch from ' + remote_output + ' ' + ref_output)
            message = colored(' - Failed to fetch from ', 'red')
            error = message + remote_output + ' ' + ref_output
            command = ['git fetch', remote, truncate_ref(ref), '--depth', str(depth), '--prune --tags']

        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError:
            if remove_dir:
                remove_directory(self.repo_path)
            if not allow_failure:
                self._print(error)
                self._exit(error)

    def get_current_timestamp(self):
        """Get current timestamp of HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        """

        try:
            return self.repo.git.log('-1', '--format=%cI')
        except GitError as err:
            message = colored(' - Failed to find current timestamp', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def is_detached(self, print_output=False):
        """Check if HEAD is detached

        .. py:function:: is_detached(print_output=False)

        :param Optional[bool] print_output: Whether to print output
        :return: True, if HEAD is detached
        :rtype: bool
        """

        if not os.path.isdir(self.repo_path):
            return False
        if self.repo.head.is_detached:
            if print_output:
                self._print(' - HEAD is detached')
            return True
        return False

    def is_dirty(self):
        """Check whether repo is dirty

        :return: True, if repo is dirty
        :rtype: bool
        """

        if not os.path.isdir(self.repo_path):
            return False

        return self.repo.is_dirty() or self._is_rebase_in_progress() or self._untracked_files()

    def new_commits(self, upstream=False):
        """Returns the number of new commits

        .. py:function:: new_commits(upstream=False)

        :param Optional[bool] upstream: Whether to find number of new upstream or local commits
        :return: Int number of new commits
        :rtype: int
        """

        try:
            local_branch = self.repo.active_branch
        except (GitError, TypeError):
            return 0
        else:
            tracking_branch = local_branch.tracking_branch()
            if local_branch is None or tracking_branch is None:
                return 0

            try:
                commits = local_branch.commit.hexsha + '...' + tracking_branch.commit.hexsha
                rev_list_count = self.repo.git.rev_list('--count', '--left-right', commits)
            except (GitError, ValueError):
                return 0
            else:
                index = 1 if upstream else 0
                return str(rev_list_count).split()[index]

    def print_branches(self, local=False, remote=False):
        """Print branches

        .. py:function:: print_branches(local=False, remote=False)

        :param Optional[bool] local: Print local branches
        :param Optional[bool] remote: Print remote branches
        """

        if local and remote:
            command = 'git branch -a'
        elif local:
            command = 'git branch'
        elif remote:
            command = 'git branch -r'
        else:
            return

        try:
            execute_command(command, self.repo_path, print_output=self._print_output)
        except ClowderError:
            message = colored(' - Failed to print branches', 'red')
            self._print(message)
            self._exit(message)

    @not_detached
    def pull(self):
        """Pull upstream changes"""

        try:
            self._print(' - Pull latest changes')
            print(self.repo.git.pull())
        except GitError as err:
            message = colored(' - Failed to pull latest changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    @not_detached
    def push(self):
        """Push changes"""

        try:
            self._print(' - Push local changes')
            print(self.repo.git.push())
        except GitError as err:
            message = colored(' - Failed to push local changes', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def sha(self, short=False):
        """Return sha for currently checked out commit

        .. py:function:: sha(short=False)

        :param Optional[bool] short: Whether to return short or long commit sha
        :return: Commit sha
        :rtype: str
        """

        if short:
            return self.repo.git.rev_parse(self.repo.head.commit.hexsha, short=True)

        return self.repo.head.commit.hexsha

    def sha_branch_remote(self, remote, branch):
        """Return sha for remote branch

        :param str remote: Remote name
        :param str branch: Remote branch name
        :return: Commit sha of remote branch
        :rtype: str
        """

        command = "git --git-dir={0}.git rev-parse {1}/{2}".format(self.repo_path, remote, branch)
        try:
            execute_command(command, self.repo_path)
        except ClowderError:
            message = colored(' - Failed to get remote sha\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message)

    def stash(self):
        """Stash current changes in repository"""

        if not self.repo.is_dirty():
            self._print(' - No changes to stash')
            return

        self._print(' - Stash current changes')
        self.repo.git.stash()

    def status(self):
        """Print  git status

        Equivalent to: ``git status``
        """

        self.repo.git.status()

    def status_verbose(self):
        """Print git status

        Equivalent to: ``git status -vv``
        """

        command = 'git status -vv'
        self._print(fmt.command(command))

        try:
            execute_command(command, self.repo_path)
        except ClowderError:
            message = colored(' - Failed to print status\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message)

    def validate_repo(self):
        """Validate repo state

        :return: True, if repo not dirty or doesn't exist on disk
        :rtype: bool
        """

        if not existing_git_repository(self.repo_path):
            return True

        return not self.is_dirty()

    def _abort_rebase(self):
        """Abort rebase"""

        if not self._is_rebase_in_progress():
            return

        try:
            self.repo.git.rebase('--abort')
        except GitError as err:
            self._print(colored(' - Failed to abort rebase', 'red'))
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _clean(self, args):
        """Clean git directory

        :param str args: Git clean args
        """

        try:
            self.repo.git.clean(args)
        except GitError as err:
            message = colored(' - Failed to clean git repo', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(fmt.error(err))
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    # def _existing_remote_tag(self, tag, remote, depth=0):
    #     """Check if remote tag exists
    #
    #     :param str tag: Tag name
    #     :param str remote: Remote name
    #     :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #         Defaults to 0
    #     :return: True, if remote tag exists
    #     :rtype: bool
    #     """
    #
    #     origin = self._remote(remote, remove_dir=True)
    #     self.fetch(remote, depth=depth, ref=tag, remove_dir=True)
    #     return tag in origin.tags

    def _exit(self, message=''):
        """Exit based on serial or parallel job

        :param Optional[str] message: Error message

        Raises:
            ClowderGitError
            ClowderExit
        """

        if self.parallel:
            raise ClowderGitError(msg=fmt.parallel_exception_error(self.repo_path, message))

        raise ClowderExit(1)

    def _is_rebase_in_progress(self):
        """Detect whether rebase is in progress

        :return: True, if rebase is in progress
        :rtype: bool
        """

        rebase_apply = os.path.join(self.repo_path, '.git', 'rebase-apply')
        rebase_merge = os.path.join(self.repo_path, '.git', 'rebase-merge')
        is_rebase_apply = os.path.isdir(rebase_apply)
        is_rebase_merge = os.path.isdir(rebase_merge)
        return is_rebase_apply or is_rebase_merge

    def _print(self, val):
        """Print output if self._print_output is True

        :param str val: Output to print
        """

        if self._print_output:
            print(val)

    def _repo(self):
        """Create Repo instance for self.repo_path

        :return: GitPython Repo instance
        :rtype: Repo
        """

        try:
            repo = Repo(self.repo_path)
        except GitError as err:
            repo_path_output = fmt.get_path(self.repo_path)
            message = colored(" - Failed to create Repo instance for ", 'red') + repo_path_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            return repo

    def _reset_head(self, branch=None):
        """Reset head of repo, discarding changes

        :param Optional[str] branch: Branch to reset head to
        """

        if branch is None:
            try:
                self.repo.head.reset(index=True, working_tree=True)
            except GitError as err:
                ref_output = fmt.ref_string('HEAD')
                message = colored(' - Failed to reset ', 'red') + ref_output
                self._print(message)
                self._print(fmt.error(err))
                self._exit(message)
            except (KeyboardInterrupt, SystemExit):
                self._exit()
            else:
                return 0

        try:
            self.repo.git.reset('--hard', branch)
        except GitError as err:
            branch_output = fmt.ref_string(branch)
            message = colored(' - Failed to reset to ', 'red') + branch_output
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            return 0

    def _untracked_files(self):
        """Check whether untracked files exist

        :return: True, if untracked files exist
        :rtype: bool
        """

        command = "git ls-files -o -d --exclude-standard | sed q | wc -l| tr -d '[:space:]'"
        try:
            output = subprocess.check_output(command, shell=True, cwd=self.repo_path)
        except GitError as err:
            message = colored(' - Failed to check untracked files', 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        else:
            return output.decode('utf-8') == '1'
