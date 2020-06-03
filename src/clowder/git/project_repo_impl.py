# -*- coding: utf-8 -*-
"""Project Git abstract utility class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os
from pathlib import Path
from typing import Dict, Optional

from git import GitError, Remote, Repo, Tag

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory

from .git_repo import GitRepo
from .util import (
    existing_git_repository,
    not_detached
)

GitConfig = Dict[str, str]


class ProjectRepoImpl(GitRepo):
    """Abstract class encapsulating private git utilities for projects

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

    def _checkout_branch(self, branch: str) -> None:
        """Checkout local branch or print message if already checked out

        :param str branch: Branch name
        """

        if self._is_branch_checked_out(branch):
            self._print(' - Branch ' + fmt.ref_string(branch) + ' already checked out')
        else:
            self._checkout_branch_local(branch)

    def _checkout_branch_local(self, branch: str, remove_dir: bool = False) -> None:
        """Checkout local branch

        :param str branch: Branch name
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(f' - Checkout branch {branch_output}')
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
        except GitError as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to checkout branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to checkout branch', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            raise

    def _checkout_new_repo_branch(self, branch: str, depth: int) -> None:
        """Checkout remote branch or fail and delete repo if it doesn't exist

        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(self.remote)
        self._remote(self.remote, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=branch, remove_dir=True)

        if not self.existing_remote_branch(branch, self.remote):
            # TODO: Handle possible exceptions
            remove_directory(self.repo_path)
            message = f'{fmt.ERROR} No existing remote branch {remote_output} {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _checkout_new_repo_commit(self, commit: str, remote: str, depth: int) -> None:
        """Checkout commit or fail and delete repo if it doesn't exist

        :param str commit: Commit sha
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        commit_output = fmt.ref_string(commit)
        self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=commit, remove_dir=True)

        self._print(' - Checkout commit ' + commit_output)
        try:
            self.repo.git.checkout(commit)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            # TODO: Handle possible exceptions
            remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to checkout commit {commit_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to checkout commit', err)
            # TODO: Handle possible exceptions
            remove_directory(self.repo_path)
            raise

    def _checkout_new_repo_tag(self, tag: str, remote: str, depth: int, remove_dir: bool = False) -> None:
        """Checkout tag or fail and delete repo if it doesn't exist

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise ClowderError:
        """

        remote_tag = self._get_remote_tag(tag, remote, depth=depth, remove_dir=remove_dir)
        if remote_tag is None:
            return

        tag_output = fmt.ref_string(tag)
        try:
            self._print(' - Checkout tag ' + tag_output)
            self.repo.git.checkout(remote_tag)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to checkout tag {tag_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to checkout tag', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            raise

    def _checkout_sha(self, sha: str) -> None:
        """Checkout commit by sha

        :param str sha: Commit sha
        :raise ClowderError:
        """

        commit_output = fmt.ref_string(sha)
        try:
            if self.repo.head.commit.hexsha == sha:
                self._print(' - On correct commit')
                return
            self._print(f' - Checkout commit {commit_output}')
            self.repo.git.checkout(sha)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to checkout commit {commit_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _checkout_tag(self, tag: str) -> None:
        """Checkout commit tag is pointing to

        :param str tag: Tag name
        :raise ClowderError:
        """

        tag_output = fmt.ref_string(tag)
        if tag not in self.repo.tags:
            message = f'{fmt.ERROR} No existing tag {tag_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                self._print(' - On correct commit for tag')
                return
            self._print(f' - Checkout tag {tag_output}')
            self.repo.git.checkout(f'refs/tags/{tag}')
        except (GitError, ValueError) as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to checkout tag {tag_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _compare_remote_url(self, remote: str, url: str) -> None:
        """Compare actual remote url to given url

        If URL's are different print error message and exit

        :param str remote: Remote name
        :param str url: URL to compare with remote's URL
        :raise ClowderError:
        """

        if url != self._remote_get_url(remote):
            actual_url = self._remote_get_url(remote)
            message = fmt.error_remote_already_exists(remote, url, actual_url)
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

    def _create_branch_local(self, branch: str) -> None:
        """Create local branch

        :param str branch: Branch name
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        try:
            self._print(f' - Create branch {branch_output}')
            self.repo.create_head(branch)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to create branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _create_branch_local_tracking(self, branch: str, remote: str, depth: int,
                                      fetch: bool = True, remove_dir: bool = False) -> None:
        """Create and checkout tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch before creating branch
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote, remove_dir=remove_dir)
        if fetch:
            self.fetch(remote, depth=depth, ref=branch, remove_dir=remove_dir)

        try:
            self._print(f' - Create branch {branch_output}')
            self.repo.create_head(branch, origin.refs[branch])
        except (GitError, IndexError) as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to create branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to create branch', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            raise
        else:
            self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch: str, remote: str, depth: int) -> None:
        """Create remote tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        self.fetch(remote, depth=depth, ref=branch)

        if branch in self._remote(remote).refs:
            self._print_existing_remote_branch_message(branch)
            return

        try:
            self._print(f' - Push remote branch {branch_output}')
            self.repo.git.push(remote, branch)
            self._set_tracking_branch(remote, branch)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to push remote branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _create_remote(self, remote: str, url: str, remove_dir: bool = False) -> None:
        """Create new remote

        :param str remote: Remote name
        :param str url: URL of repo
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise ClowderError:
        """

        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return

        remote_output = fmt.remote_string(remote)
        try:
            self._print(f' - Create remote {remote_output}')
            self.repo.create_remote(remote, url)
            return
        except GitError as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to create remote {remote_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to create remote', err)
            if remove_dir:
                # TODO: Handle possible exceptions
                remove_directory(self.repo_path)
            raise

    def _find_rev_by_timestamp(self, timestamp: str, ref: str) -> str:
        """Find rev by timestamp

        :param str timestamp: Commit ref timestamp
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp
        :rtype: str
        :raise ClowderError:
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, ref)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to find revision from timestamp'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _find_rev_by_timestamp_author(self, timestamp: str, author: str, ref: str) -> str:
        """Find rev by timestamp and author

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp by author
        :rtype: str
        :raise ClowderError:
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, '--author', author, ref)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to find revision from timestamp by author'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _get_remote_tag(self, tag: str, remote: str, depth: int = 0,
                        remove_dir: bool = False) -> Optional[Tag]:
        """Returns Tag object

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool remove_dir: Whether to remove the directory if commands fail
        :return: GitPython Tag object if it exists, otherwise None
        :rtype: Optional[Tag]
        :raise ClowderError:
        """

        tag_output = fmt.ref_string(tag)
        self._remote(remote, remove_dir=remove_dir)
        self.fetch(remote, depth=depth, ref=f'refs/tags/{tag}', remove_dir=remove_dir)

        try:
            return self.repo.tags[tag]
        except (GitError, IndexError) as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} No existing tag {tag_output}'
            if remove_dir:
                # TODO: Handle possible exceptions raised here
                remove_directory(self.repo_path)
                message = self._format_error_message(message)
                raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
            if self._print_output:
                self._print(message)
            return None
        except Exception as err:
            LOG_DEBUG('Failed to get tag', err)
            if remove_dir:
                # TODO: Handle possible exceptions raised here
                remove_directory(self.repo_path)
            raise

    def _init_repo(self) -> None:
        """Initialize repository

        Raises:
             ClowderError
             OSError
        """

        if existing_git_repository(self.repo_path):
            # TODO: Raise exception here?
            return

        try:
            self._print(f' - Initialize repo at {fmt.path_string(str(self.repo_path))}')
            if not self.repo_path.is_dir():
                try:
                    os.makedirs(str(self.repo_path))
                except OSError as err:
                    LOG_DEBUG('Failed to create directory', err)
                    if err.errno != errno.EEXIST:
                        raise
            self.repo = Repo.init(self.repo_path)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            # TODO: Handle possible exceptions
            remove_directory(self.repo_path)
            message = f'{fmt.ERROR} Failed to initialize repository'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to initialize repository', err)
            remove_directory(self.repo_path)
            raise

    def _is_branch_checked_out(self, branch: str) -> bool:
        """Check if branch is checked out

        :param str branch: Branch name
        :return: True, if branch is checked out
        :rtype: bool
        :raise ClowderError:
        """

        try:
            default_branch = self.repo.heads[branch]
            is_detached = self.repo.head.is_detached
            same_branch = self.repo.head.ref == default_branch
            return not is_detached and same_branch
        except (GitError, TypeError):
            return False

    def _is_tracking_branch(self, branch: str) -> bool:
        """Check if branch is a tracking branch

        :param str branch: Branch name
        :return: True, if branch has a tracking relationship
        :rtype: bool
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        try:
            local_branch = self.repo.heads[branch]
            tracking_branch = local_branch.tracking_branch()
            return True if tracking_branch else False
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} No existing branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _print_existing_remote_branch_message(self, branch: str) -> None:
        """Print output message for existing remote branch

        :param str branch: Branch name
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        try:
            self.repo.git.config('--get', 'branch.' + branch + '.merge')
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Remote branch {branch_output} already exists'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        else:
            self._print(f' - Tracking branch {branch_output} already exists')

    @not_detached
    def _pull(self, remote: str, branch: str) -> None:
        """Pull from remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(f' - Pull from {remote_output} {branch_output}')
        try:
            execute_command(f"git pull {remote} {branch}", self.repo_path, print_output=self._print_output)
        except ClowderError as err:
            LOG_DEBUG('Failed to pull', err)
            message = f'{fmt.ERROR} Failed to pull from {remote_output} {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    @not_detached
    def _rebase_remote_branch(self, remote: str, branch: str) -> None:
        """Rebase onto remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        self._print(f' - Rebase onto {remote_output} {branch_output}')
        try:
            execute_command(f"git pull {remote} {branch} --rebase", self.repo_path, print_output=self._print_output)
        except ClowderError as err:
            LOG_DEBUG('Failed pull with rebase', err)
            message = f'{fmt.ERROR} Failed to rebase onto {remote_output} {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _remote(self, remote: str, remove_dir: bool = False) -> Remote:
        """Get GitPython Remote instance

        :param str remote: Remote name
        :param bool remove_dir: Whether to remove the directory if commands fail
        :return: GitPython Remote instance
        :rtype: Remote
        :raise ClowderError:
        """

        remote_output = fmt.remote_string(remote)
        try:
            return self.repo.remotes[remote]
        except GitError as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                # TODO: Handle possible exceptions raised here
                remove_directory(self.repo_path)
            message = f'{fmt.ERROR} No existing remote {remote_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _remote_get_url(self, remote: str) -> str:
        """Get url of remote

        :param str remote: Remote name
        :return: URL of remote
        :rtype: str
        """

        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from: str, remote_to: str) -> None:
        """Rename remote

        :param str remote_from: Name of remote to rename
        :param str remote_to: Name to rename remote to
        :raise ClowderError:
        """

        remote_output_f = fmt.remote_string(remote_from)
        remote_output_t = fmt.remote_string(remote_to)
        self._print(f' - Rename remote {remote_output_f} to {remote_output_t}')
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            message = f'{fmt.ERROR} Failed to rename remote from {remote_output_f} to {remote_output_t}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)

    def _set_tracking_branch(self, remote: str, branch: str, remove_dir: bool = False) -> None:
        """Set tracking branch

        :param str remote: Remote name
        :param str branch: Branch name
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        remote_output = fmt.remote_string(remote)
        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            self._print(f' - Set tracking branch {branch_output} -> {remote_output} {branch_output}')
            local_branch.set_tracking_branch(remote_branch)
        except GitError as err:
            LOG_DEBUG('Git error', err)
            if remove_dir:
                # TODO: Handle possible exceptions raised here
                remove_directory(self.repo_path)
            message = f' - Failed to set tracking branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message, error=err)
        except Exception as err:
            LOG_DEBUG('Failed to set tracking branch', err)
            if remove_dir:
                remove_directory(self.repo_path)
            raise

    def _set_tracking_branch_commit(self, branch: str, remote: str, depth: int) -> None:
        """Set tracking relationship between local and remote branch if on same commit

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderError:
        """

        branch_output = fmt.ref_string(branch)
        origin = self._remote(remote)
        self.fetch(remote, depth=depth, ref=branch)

        if not self.existing_local_branch(branch):
            message = f'{fmt.ERROR} No local branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        if not self.existing_remote_branch(branch, remote):
            message = f'{fmt.ERROR} No remote branch {branch_output}'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            message = f' - Existing remote branch {branch_output} on different commit'
            message = self._format_error_message(message)
            raise ClowderError(ClowderErrorType.GIT_ERROR, message)

        self._set_tracking_branch(remote, branch)

    def _update_git_config(self, config: GitConfig) -> None:
        """Update custom git config

        :param GitConfig config: Custom git config
        :raise ClowderError:
        """

        self._print(" - Update git config")
        for key, value in config.items():
            self.git_config_unset_all_local(key)
            self.git_config_add_local(key, value)
