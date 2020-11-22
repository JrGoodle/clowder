"""Project Git abstract utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, Optional

from git import GitError, Remote, Repo, Tag

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.error import ClowderGitError
from clowder.logging import LOG
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory, make_dir

from .git_ref import GitRef
from .git_repo import GitRepo
from .util import (
    existing_git_repo,
    not_detached
)

GitConfig = Dict[str, str]


class ProjectRepoImpl(GitRepo):
    """Abstract class encapsulating private git utilities for projects

    :ivar str repo_path: Absolute path to repo
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str):
        """ProjectRepo __init__

        :param Path repo_path: Absolute path to repo
        :param str remote: Default remote name
        """

        super().__init__(repo_path, remote)

    def _checkout_branch(self, branch: str) -> None:
        """Checkout local branch or print message if already checked out

        :param str branch: Branch name
        """

        if self._is_branch_checked_out(branch):
            CONSOLE.stdout(f' - Branch {fmt.ref(branch)} already checked out')
        else:
            self._checkout_branch_local(branch)

    def _checkout_branch_local(self, branch: str, remove_dir: bool = False) -> None:
        """Checkout local branch

        :param str branch: Branch name
        :param bool remove_dir: Whether to remove the directory if commands fail
        :raise:
        """

        try:
            CONSOLE.stdout(f' - Checkout branch {fmt.ref(branch)}')
            default_branch = self.repo.heads[branch]
            default_branch.checkout()
        except BaseException:
            CONSOLE.stderr(f'Failed to checkout branch {fmt.ref(branch)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _checkout_new_repo_branch(self, branch: str, depth: int) -> None:
        """Checkout remote branch or fail and delete repo if it doesn't exist

        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderGitError:
        """

        self._remote(self.remote, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=GitRef(branch=branch), remove_dir=True)

        if not self.has_remote_branch(branch, self.remote):
            remove_directory(self.repo_path, check=False)
            raise ClowderGitError(f'No existing remote branch {fmt.remote(self.remote)} {fmt.ref(branch)}')

        self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

    def _checkout_new_repo_commit(self, commit: str, remote: str, depth: int) -> None:
        """Checkout commit or fail and delete repo if it doesn't exist

        :param str commit: Commit sha
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._remote(remote, remove_dir=True)
        self.fetch(remote, depth=depth, ref=GitRef(commit=commit), remove_dir=True)

        CONSOLE.stdout(f' - Checkout commit {fmt.ref(commit)}')
        try:
            self.repo.git.checkout(commit)
        except BaseException:
            CONSOLE.stderr(f'Failed to checkout commit {fmt.ref(commit)}')
            remove_directory(self.repo_path, check=False)
            raise

    def _checkout_new_repo_tag(self, tag: str, remote: str, depth: int, remove_dir: bool = False) -> None:
        """Checkout tag or fail and delete repo if it doesn't exist

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool remove_dir: Whether to remove the directory if commands fail
        """

        remote_tag = self._get_remote_tag(tag, remote, depth=depth, remove_dir=remove_dir)
        if remote_tag is None:
            return

        try:
            CONSOLE.stdout(f' - Checkout tag {fmt.ref(tag)}')
            self.repo.git.checkout(remote_tag)
        except BaseException:
            CONSOLE.stderr(f'Failed to checkout tag {fmt.ref(tag)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _checkout_sha(self, sha: str) -> None:
        """Checkout commit by sha

        :param str sha: Commit sha
        """

        try:
            if self.repo.head.commit.hexsha == sha:
                CONSOLE.stdout(' - On correct commit')
                return
            CONSOLE.stdout(f' - Checkout commit {fmt.ref(sha)}')
            self.repo.git.checkout(sha)
        except GitError:
            CONSOLE.stderr(f'Failed to checkout commit {fmt.ref(sha)}')
            raise

    def _checkout_tag(self, tag: str) -> None:
        """Checkout commit tag is pointing to

        :param str tag: Tag name
        :raise ClowderGitError:
        """

        if tag not in self.repo.tags:
            raise ClowderGitError(f'No existing tag {fmt.ref(tag)}')

        try:
            same_commit = self.repo.head.commit == self.repo.tags[tag].commit
            is_detached = self.repo.head.is_detached
            if same_commit and is_detached:
                CONSOLE.stdout(' - On correct commit for tag')
                return
            CONSOLE.stdout(f' - Checkout tag {fmt.ref(tag)}')
            self.repo.git.checkout(f'refs/tags/{tag}')
        except (GitError, ValueError):
            CONSOLE.stderr(f'Failed to checkout tag {fmt.ref(tag)}')
            raise

    def _compare_remote_url(self, remote: str, url: str) -> None:
        """Compare actual remote url to given url

        If URL's are different print error message and exit

        :param str remote: Remote name
        :param str url: URL to compare with remote's URL
        :raise ClowderGitError:
        """

        if url != self._remote_get_url(remote):
            actual_url = self._remote_get_url(remote)
            message = f"Remote {fmt.remote(remote)} already exists with a different url\n" \
                      f"{fmt.url_string(actual_url)} should be {fmt.url_string(url)}"
            raise ClowderGitError(message)

    def _create_branch_local(self, branch: str) -> None:
        """Create local branch

        :param str branch: Branch name
        """

        try:
            CONSOLE.stdout(f' - Create branch {fmt.ref(branch)}')
            self.repo.create_head(branch)
        except GitError:
            CONSOLE.stderr(f'Failed to create branch {fmt.ref(branch)}')
            raise

    def _create_branch_local_tracking(self, branch: str, remote: str, depth: int,
                                      fetch: bool = True, remove_dir: bool = False) -> None:
        """Create and checkout tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch before creating branch
        :param bool remove_dir: Whether to remove the directory if commands fail
        """

        origin = self._remote(remote, remove_dir=remove_dir)
        if fetch:
            self.fetch(remote, depth=depth, ref=GitRef(branch=branch), remove_dir=remove_dir)

        try:
            CONSOLE.stdout(f' - Create branch {fmt.ref(branch)}')
            self.repo.create_head(branch, origin.refs[branch])
        except BaseException:
            CONSOLE.stderr(f'Failed to create branch {fmt.ref(branch)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise
        else:
            self._set_tracking_branch(remote, branch, remove_dir=remove_dir)
            self._checkout_branch_local(branch, remove_dir=remove_dir)

    def _create_branch_remote_tracking(self, branch: str, remote: str, depth: int) -> None:
        """Create remote tracking branch

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self.fetch(remote, depth=depth, ref=GitRef(branch=branch))

        if branch in self._remote(remote).refs:
            self._print_has_remote_branch_message(branch)
            return

        try:
            CONSOLE.stdout(f' - Push remote branch {fmt.ref(branch)}')
            self.repo.git.push(remote, branch)
            self._set_tracking_branch(remote, branch)
        except GitError:
            CONSOLE.stderr(f'Failed to push remote branch {fmt.ref(branch)}')
            raise

    def _create_remote(self, remote: str, url: str, remove_dir: bool = False) -> None:
        """Create new remote

        :param str remote: Remote name
        :param str url: URL of repo
        :param bool remove_dir: Whether to remove the directory if commands fail
        """

        remote_names = [r.name for r in self.repo.remotes]
        if remote in remote_names:
            return

        try:
            CONSOLE.stdout(f' - Create remote {fmt.remote(remote)}')
            self.repo.create_remote(remote, url)
        except BaseException:
            CONSOLE.stderr(f'Failed to create remote {fmt.remote(remote)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _find_rev_by_timestamp(self, timestamp: str, ref: str) -> str:
        """Find rev by timestamp

        :param str timestamp: Commit ref timestamp
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, ref)
        except GitError:
            CONSOLE.stderr('Failed to find revision from timestamp')
            raise

    def _find_rev_by_timestamp_author(self, timestamp: str, author: str, ref: str) -> str:
        """Find rev by timestamp and author

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        :return: Commit sha at or before timestamp by author
        """

        try:
            return self.repo.git.log('-1', '--format=%H', '--before=' + timestamp, '--author', author, ref)
        except GitError:
            CONSOLE.stderr('Failed to find revision from timestamp by author')
            raise

    def _get_remote_tag(self, tag: str, remote: str, depth: int = 0, remove_dir: bool = False) -> Optional[Tag]:
        """Returns Tag object

        :param str tag: Tag name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool remove_dir: Whether to remove the directory if commands fail
        :return: GitPython Tag object if it exists, otherwise None
        """

        self._remote(remote, remove_dir=remove_dir)
        self.fetch(remote, depth=depth, ref=GitRef(tag=tag), remove_dir=remove_dir)

        try:
            return self.repo.tags[tag]
        except (GitError, IndexError) as err:
            CONSOLE.stderr(f'No existing tag {fmt.ref(tag)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
                raise
            LOG.debug(error=err)
            return None
        except BaseException:
            CONSOLE.stderr('Failed to get tag')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _init_repo(self) -> None:
        """Initialize repository"""

        if existing_git_repo(self.repo_path):
            # TODO: Raise exception here?
            return

        try:
            CONSOLE.stdout(f' - Initialize repo at {fmt.path(self.repo_path)}')
            if not self.repo_path.is_dir():
                make_dir(self.repo_path)
            self.repo = Repo.init(self.repo_path)
        except BaseException:
            CONSOLE.stderr('Failed to initialize repository')
            remove_directory(self.repo_path, check=False)
            raise

    def _is_branch_checked_out(self, branch: str) -> bool:
        """Check if branch is checked out

        :param str branch: Branch name
        :return: True, if branch is checked out
        """

        try:
            default_branch = self.repo.heads[branch]
            is_detached = self.repo.head.is_detached
            same_branch = self.repo.head.ref == default_branch
            return not is_detached and same_branch
        except (GitError, TypeError) as err:
            LOG.debug(error=err)
            return False

    def _is_tracking_branch(self, branch: str) -> bool:
        """Check if branch is a tracking branch

        :param str branch: Branch name
        :return: True, if branch has a tracking relationship
        """

        try:
            local_branch = self.repo.heads[branch]
            tracking_branch = local_branch.tracking_branch()
            return True if tracking_branch else False
        except GitError:
            CONSOLE.stderr(f'No existing branch {fmt.ref(branch)}')
            raise

    def _print_has_remote_branch_message(self, branch: str) -> None:
        """Print output message for existing remote branch

        :param str branch: Branch name
        """

        try:
            self.repo.git.config('--get', 'branch.' + branch + '.merge')
            CONSOLE.stdout(f' - Tracking branch {fmt.ref(branch)} already exists')
        except GitError:
            CONSOLE.stderr(f'Remote branch {fmt.ref(branch)} already exists')
            raise

    @not_detached
    def _pull(self, remote: str, branch: str) -> None:
        """Pull from remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        """

        CONSOLE.stdout(f' - Pull from {fmt.remote(remote)} {fmt.ref(branch)}')
        try:
            execute_command(f"git pull {remote} {branch}", self.repo_path)
        except CalledProcessError:
            CONSOLE.stderr(f'Failed to pull from {fmt.remote(remote)} {fmt.ref(branch)}')
            raise

    @not_detached
    def _rebase_remote_branch(self, remote: str, branch: str) -> None:
        """Rebase onto remote branch

        :param str remote: Remote name
        :param str branch: Branch name
        """

        CONSOLE.stdout(f' - Rebase onto {fmt.remote(remote)} {fmt.ref(branch)}')
        try:
            command = f"git pull --rebase {remote} refs/heads/{branch}:refs/remotes/{remote}/heads/{branch}"
            execute_command(command, self.repo_path)
        except CalledProcessError:
            CONSOLE.stderr(f'Failed to rebase onto {fmt.remote(remote)} {fmt.ref(branch)}')
            raise

    def _remote(self, remote: str, remove_dir: bool = False) -> Remote:
        """Get GitPython Remote instance

        :param str remote: Remote name
        :param bool remove_dir: Whether to remove the directory if commands fail
        :return: GitPython Remote instance
        """

        try:
            return self.repo.remotes[remote]
        except GitError:
            CONSOLE.stderr(f'No existing remote {fmt.remote(remote)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _remote_get_url(self, remote: str) -> str:
        """Get url of remote

        :param str remote: Remote name
        :return: URL of remote
        """

        return self.repo.git.remote('get-url', remote)

    def _rename_remote(self, remote_from: str, remote_to: str) -> None:
        """Rename remote

        :param str remote_from: Name of remote to rename
        :param str remote_to: Name to rename remote to
        """

        CONSOLE.stdout(f' - Rename remote {fmt.remote(remote_from)} to {fmt.remote(remote_to)}')
        try:
            self.repo.git.remote('rename', remote_from, remote_to)
        except GitError:
            CONSOLE.stderr(f'Failed to rename remote from {fmt.remote(remote_from)} to {fmt.remote(remote_to)}')
            raise

    def _set_tracking_branch(self, remote: str, branch: str, remove_dir: bool = False) -> None:
        """Set tracking branch

        :param str remote: Remote name
        :param str branch: Branch name
        :param bool remove_dir: Whether to remove the directory if commands fail
        """

        origin = self._remote(remote)
        try:
            local_branch = self.repo.heads[branch]
            remote_branch = origin.refs[branch]
            CONSOLE.stdout(f' - Set tracking branch {fmt.ref(branch)} -> {fmt.remote(remote)} {fmt.ref(branch)}')
            local_branch.set_tracking_branch(remote_branch)
        except BaseException:
            CONSOLE.stderr(f' - Failed to set tracking branch {fmt.ref(branch)}')
            if remove_dir:
                remove_directory(self.repo_path, check=False)
            raise

    def _set_tracking_branch_commit(self, branch: str, remote: str, depth: int) -> None:
        """Set tracking relationship between local and remote branch if on same commit

        :param str branch: Branch name
        :param str remote: Remote name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderGitError:
        """

        origin = self._remote(remote)
        self.fetch(remote, depth=depth, ref=GitRef(branch=branch))

        if not self.has_local_branch(branch):
            raise ClowderGitError(f'No local branch {fmt.ref(branch)}')

        if not self.has_remote_branch(branch, remote):
            raise ClowderGitError(f'No remote branch {fmt.ref(branch)}')

        local_branch = self.repo.heads[branch]
        remote_branch = origin.refs[branch]
        if local_branch.commit != remote_branch.commit:
            raise ClowderGitError(f' - Existing remote branch {fmt.ref(branch)} on different commit')

        self._set_tracking_branch(remote, branch)

    def _update_git_config(self, config: GitConfig) -> None:
        """Update custom git config

        :param GitConfig config: Custom git config
        """

        CONSOLE.stdout(" - Update git config")
        for key, value in config.items():
            self.git_config_unset_all_local(key)
            self.git_config_add_local(key, value)
