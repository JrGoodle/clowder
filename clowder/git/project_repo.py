"""Project Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from git import GitError
import pygoodle.filesystem as fs
from pygoodle.connectivity import is_offline
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.util.error import ClowderGitError, UnknownTypeError

from .git_ref import GitRef, GitRefEnum
from .project_repo_impl import GitConfig, ProjectRepoImpl
from .util import existing_git_repo


class ProjectRepo(ProjectRepoImpl):
    """Class encapsulating git utilities for projects

    :ivar str repo_path: Absolute path to repo
    :ivar GitRef default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, repo_path: Path, remote: str, default_ref: GitRef):
        """ProjectRepo __init__

        :param Path repo_path: Absolute path to repo
        :param str remote: Default remote name
        :param GitRef default_ref: Default ref
        """

        super().__init__(repo_path, remote)

        self.default_ref: GitRef = default_ref

    def create_clowder_repo(self, url: str, branch: str, depth: int = 0) -> None:
        """Clone clowder git repo from url at path

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ExistingFileError:
        """

        if existing_git_repo(self.repo_path):
            # TODO: Throw error if repo doesn't match one trying to create
            return

        if self.repo_path.is_dir():
            try:
                self.repo_path.rmdir()
            except OSError:
                LOG.error(f"Directory already exists at {fmt.path(self.repo_path)}")
                raise

        if self.repo_path.is_symlink():
            fs.remove_file(self.repo_path)
        else:
            from clowder.environment import ENVIRONMENT
            if ENVIRONMENT.existing_clowder_repo_file_error:
                raise ENVIRONMENT.existing_clowder_repo_file_error

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, remote_name: str, remote_url: str,
                          upstream_remote_name: str, upstream_remote_url: str) -> None:
        """Configure remotes names for project and upstream

        :param str remote_name: Project remote name
        :param str remote_url: Project remote url
        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        """

        if not existing_git_repo(self.repo_path):
            return

        try:
            remotes = self.repo.remotes
        except GitError as err:
            LOG.debug('No remotes', err)
            return
        else:
            for remote in remotes:
                if remote_url == self._remote_get_url(remote.name) and remote.name != remote_name:
                    self._rename_remote(remote.name, remote_name)
                    continue
                if upstream_remote_url == self._remote_get_url(remote.name) and remote.name != upstream_remote_name:
                    self._rename_remote(remote.name, upstream_remote_name)
            self._compare_remotes(remote_name, remote_url, upstream_remote_name, upstream_remote_url)

    def herd(self, url: str, depth: int = 0, fetch: bool = True,
             rebase: bool = False, config: Optional[GitConfig] = None) -> None:
        """Herd ref

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[GitConfig] config: Custom git config
        """

        if not existing_git_repo(self.repo_path):
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
                    upstream_remote: Optional[str] = None, config: Optional[GitConfig] = None) -> None:
        """Herd branch

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[str] upstream_remote: Upstream remote name
        :param Optional[GitConfig] config: Custom git config
        """

        if not existing_git_repo(self.repo_path):
            self._herd_branch_initial(url, branch, depth=depth)
            self.install_project_git_herd_alias()
            if config is not None:
                self._update_git_config(config)
            return

        if config is not None:
            self.install_project_git_herd_alias()
            self._update_git_config(config)

        if self.has_local_branch(branch):
            self._herd_branch_existing_local(branch, depth=depth, rebase=rebase, upstream_remote=upstream_remote)
            return

        branch_ref = GitRef(branch=branch)
        self.fetch(self.remote, depth=depth, ref=branch_ref, allow_failure=True)
        if self.has_remote_branch(branch, self.remote):
            self._herd(self.remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
            return

        CONSOLE.stdout(f' - No existing remote branch {fmt.remote(self.remote)} {fmt.ref(branch)}')
        if upstream_remote:
            self.fetch(upstream_remote, depth=depth, ref=branch_ref)
            if self.has_remote_branch(branch, upstream_remote):
                self._herd(upstream_remote, branch_ref, depth=depth, fetch=False, rebase=rebase)
                return
            CONSOLE.stdout(f' - No existing remote branch {fmt.remote(upstream_remote)} {fmt.ref(branch)}')

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

        fetch = depth != 0

        if not existing_git_repo(self.repo_path):
            self._init_repo()
            self._create_remote(self.remote, url, remove_dir=True)
            try:
                self._checkout_new_repo_tag(tag, self.remote, depth)
            except Exception as err:
                LOG.debug('Failed checkout new repo tag', err)
                self.herd(url, depth=depth, fetch=fetch, rebase=rebase)
                return

        self.install_project_git_herd_alias()
        if config is not None:
            self._update_git_config(config)
        try:
            self.fetch(self.remote, ref=GitRef(tag=tag), depth=depth)
            self._checkout_tag(tag)
        except Exception as err:
            LOG.debug('Failed fetch and checkout tag', err)
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
            self.fetch(remote, ref=GitRef(branch=branch))
        except Exception as err:
            LOG.debug('Failed fetch', err)
            self.fetch(remote, ref=self.default_ref)

    def install_project_git_herd_alias(self) -> None:
        """Install 'git herd' alias for project"""

        from clowder.environment import ENVIRONMENT

        config_variable = 'alias.herd'
        config_value = f'!clowder herd {self.repo_path.relative_to(ENVIRONMENT.clowder_dir)}'
        CONSOLE.stdout(" - Update git herd alias")
        self.git_config_unset_all_local(config_variable)
        self.git_config_add_local(config_variable, config_value)

    def prune_branch_local(self, branch: str, force: bool) -> None:
        """Prune local branch

        :param str branch: Branch name to delete
        :param bool force: Force delete branch
        """

        if branch not in self.repo.heads:
            CONSOLE.stdout(f" - Local branch {fmt.ref(branch)} doesn't exist")
            return

        prune_branch = self.repo.heads[branch]
        if self.repo.head.ref == prune_branch:
            try:
                CONSOLE.stdout(f' - Checkout ref {fmt.ref(self.default_ref.short_ref)}')
                self.repo.git.checkout(self.default_ref.short_ref)
            except GitError:
                LOG.error(f'Failed to checkout ref {fmt.ref(self.default_ref.short_ref)}')
                raise

        try:
            CONSOLE.stdout(f' - Delete local branch {fmt.ref(branch)}')
            self.repo.delete_head(branch, force=force)
        except GitError:
            LOG.error(f'Failed to delete local branch {fmt.ref(branch)}')
            raise

    def prune_branch_remote(self, branch: str, remote: str) -> None:
        """Prune remote branch in repository

        :param str branch: Branch name to delete
        :param str remote: Remote name
        """

        if not self.has_remote_branch(branch, remote):
            CONSOLE.stdout(f" - Remote branch {fmt.ref(branch)} doesn't exist")
            return

        try:
            CONSOLE.stdout(f' - Delete remote branch {fmt.ref(branch)}')
            self.repo.git.push(remote, '--delete', branch)
        except GitError:
            LOG.error(f'Failed to delete remote branch {fmt.ref(branch)}')
            raise

    def reset(self, depth: int = 0) -> None:
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :raise ClowderGitError:
        :raise UnknownTypeError:
        """

        if self.default_ref.ref_type is GitRefEnum.TAG:
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_tag(self.default_ref.short_ref)
        elif self.default_ref.ref_type is GitRefEnum.COMMIT:
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            self._checkout_sha(self.default_ref.short_ref)
        elif self.default_ref.ref_type is GitRefEnum.BRANCH:
            branch = self.default_ref.short_ref
            if not self.has_local_branch(branch):
                self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=True)
                return
            self._checkout_branch(branch)
            if not self.has_remote_branch(branch, self.remote):
                raise ClowderGitError(f'No existing remote branch {fmt.remote(self.remote)} {fmt.ref(branch)}')
            self.fetch(self.remote, ref=self.default_ref, depth=depth)
            CONSOLE.stdout(f' - Reset branch {fmt.ref(branch)} to {fmt.remote(self.remote)} {fmt.ref(branch)}')
            self._reset_head(branch=f'{self.remote}/{branch}')
        else:
            raise UnknownTypeError('Unknown GitRefEnum type')

    def reset_timestamp(self, timestamp: str, author: str, ref: str) -> None:
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param str timestamp: Commit ref timestamp
        :param str author: Commit author
        :param str ref: Reference ref
        :raise ClowderGitError:
        """

        rev = None
        if author:
            rev = self._find_rev_by_timestamp_author(timestamp, author, ref)
        if not rev:
            rev = self._find_rev_by_timestamp(timestamp, ref)
        if not rev:
            raise ClowderGitError(f'Failed to find revision')

        self._checkout_sha(rev)

    def start(self, remote: str, branch: str, depth: int, tracking: bool) -> None:
        """Start new branch in repository and checkout

        :param str remote: Remote name
        :param str branch: Local branch name to create
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        if branch not in self.repo.heads:
            if not is_offline():
                self.fetch(remote, ref=GitRef(branch=branch), depth=depth)
            try:
                self._create_branch_local(branch)
                self._checkout_branch_local(branch)
            except BaseException as err:
                LOG.debug('Failed to create and checkout branch', err)
                raise
        else:
            CONSOLE.stdout(f' - {fmt.ref(branch)} already exists')
            if self._is_branch_checked_out(branch):
                CONSOLE.stdout(' - On correct branch')
            else:
                self._checkout_branch_local(branch)

        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def _compare_remotes(self, remote_name: str, remote_url: str,
                         upstream_remote_name: str, upstream_remote_url: str) -> None:
        """Compare remotes names for  and upstream

        :param str remote_name: Project remote name
        :param str remote_url: Project remote url
        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        """

        remote_names = [r.name for r in self.repo.remotes]
        if remote_name in remote_names:
            self._compare_remote_url(remote_name, remote_url)
        if upstream_remote_name in remote_names:
            self._compare_remote_url(upstream_remote_name, upstream_remote_url)

    def _herd(self, remote: str, ref: GitRef, depth: int = 0, fetch: bool = True, rebase: bool = False) -> None:
        """Herd ref

        :param str remote: Remote name
        :param GitRef ref: Git ref
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :raise UnknownTypeError:
        """

        if ref.ref_type == GitRefEnum.TAG:
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_tag(ref.short_ref)
        elif ref.ref_type == GitRefEnum.COMMIT:
            self.fetch(remote, depth=depth, ref=ref)
            self._checkout_sha(ref.formatted_ref)
        elif ref.ref_type == GitRefEnum.BRANCH:
            branch = ref.short_ref
            if not self.has_local_branch(branch):
                self._create_branch_local_tracking(branch, remote, depth=depth, fetch=fetch)
                return
            self._herd_existing_local(remote, branch, depth=depth, rebase=rebase)
        else:
            raise UnknownTypeError('Unknown GitRefEnum type')

    def _herd_branch_existing_local(self, branch: str, depth: int = 0, rebase: bool = False,
                                    upstream_remote: Optional[str] = None) -> None:
        """Herd branch for existing local branch

        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[str] upstream_remote: Upstream remote name
        """

        self._checkout_branch(branch)

        branch_ref = GitRef(branch=branch)
        self.fetch(self.remote, depth=depth, ref=branch_ref)
        if self.has_remote_branch(branch, self.remote):
            self._herd_remote_branch(self.remote, branch, depth=depth, rebase=rebase)
            return

        if upstream_remote:
            self.fetch(upstream_remote, depth=depth, ref=branch_ref)
            if self.has_remote_branch(branch, upstream_remote):
                self._herd_remote_branch(upstream_remote, branch, depth=depth, rebase=rebase)

    def _herd_branch_initial(self, url: str, branch: str, depth: int = 0) -> None:
        """Herd branch initial

        :param str url: URL of repo
        :param str branch: Branch name to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        self.fetch(self.remote, depth=depth, ref=GitRef(branch=branch))
        if not self.has_remote_branch(branch, self.remote):
            CONSOLE.stdout(f' - No existing remote branch {fmt.remote(self.remote)} {fmt.ref(branch)}')
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

        if not self.has_remote_branch(branch, remote):
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
        :raise UnknownTypeError:
        """

        self._init_repo()
        self._create_remote(self.remote, url, remove_dir=True)
        if self.default_ref.ref_type is GitRefEnum.BRANCH:
            self._checkout_new_repo_branch(self.default_ref.short_ref, depth)
        elif self.default_ref.ref_type is GitRefEnum.TAG:
            self._checkout_new_repo_tag(self.default_ref.short_ref, self.remote, depth, remove_dir=True)
        elif self.default_ref.ref_type is GitRefEnum.COMMIT:
            self._checkout_new_repo_commit(self.default_ref.short_ref, self.remote, depth)
        else:
            raise UnknownTypeError('Unknown GitRefEnum type')

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
