"""Project Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

# import pygoodle.filesystem as fs
# import pygoodle.git as git
from pygoodle.format import Format
from pygoodle.git import GitConfig, Ref, Remote, Repo
from pygoodle.connectivity import is_offline
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.util.error import UnknownTypeError


class ProjectRepo:
    """Class encapsulating git utilities for projects

    :ivar str repo_path: Absolute path to repo
    :ivar GitRef default_ref: Default ref
    :ivar str remote: Default remote name
    :ivar Repo Optional[repo]: Repo instance
    """

    def __init__(self, path: Path, default_remote: Remote, default_ref: Ref, depth: Optional[int] = None,
                 recursive: bool = False, rebase: bool = False, upstream_remote: Optional[Remote] = None,
                 fetch: bool = False, config: Optional[GitConfig] = None):
        """ProjectRepo __init__

        :param Path path: Absolute path to repo
        :param Remote default_remote: Default remote name
        :param Ref default_ref: Default ref
        """

        self.path: Path = path
        self.repo: Repo = Repo(path, default_remote=default_remote)
        self.default_ref: Ref = default_ref
        self.depth: Optional[int] = depth
        self.recursive: bool = recursive
        self.rebase: bool = rebase
        self.upstream_remote: Optional[Remote] = upstream_remote
        self.fetch: bool = fetch
        self.config: Optional[GitConfig] = config

    # def create_clowder_repo(self, url: str, branch: str, depth: int = 0) -> None:
    #     """Clone clowder git repo from url at path
    #
    #     :param str url: URL of repo
    #     :param str branch: Branch name
    #     :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #     :raise ExistingFileError:
    #     """
    #
    #     if self.repo.exists:
    #         # TODO: Throw error if repo doesn't match one trying to create
    #         return
    #
    #     if self.repo_path.is_dir():
    #         try:
    #             self.repo_path.rmdir()
    #         except OSError:
    #             LOG.error(f"Directory already exists at {fmt.path(self.repo_path)}")
    #             raise
    #
    #     if self.repo_path.is_symlink():
    #         fs.remove_file(self.repo_path)
    #     else:
    #         from clowder.environment import ENVIRONMENT
    #         if ENVIRONMENT.existing_clowder_repo_file_error:
    #             raise ENVIRONMENT.existing_clowder_repo_file_error
    #
    #     self._init_repo()
    #     self._create_remote(self.remote, url, remove_dir=True)
    #     self._checkout_new_repo_branch(branch, depth)

    def configure_remotes(self, remote_name: str, remote_url: str,
                          upstream_remote_name: str, upstream_remote_url: str) -> None:
        """Configure remotes names for project and upstream

        :param str remote_name: Project remote name
        :param str remote_url: Project remote url
        :param str upstream_remote_name: Upstream remote name
        :param str upstream_remote_url: Upstream remote url
        """

        if not self.repo.exists:
            return

        for remote in self.repo.remotes:
            if remote_url == remote.fetch_url and remote.name != remote_name:
                remote.rename(remote_name)
                continue
            if upstream_remote_url == remote.fetch_url and remote.name != upstream_remote_name:
                remote.rename(upstream_remote_name)
        self._compare_remotes(remote_name, remote_url, upstream_remote_name, upstream_remote_url)

    @property
    def formatted_name(self) -> str:
        """Formatted project name"""

        if not self.repo.exists:
            return str(self.path)

        if not self.repo.is_valid():
            return f'{self.path}*'
        else:
            return str(self.path)

    @staticmethod
    def colored_name(project: str) -> str:
        """Return formatted colored project name

        :param str project: Relative project path
        :return: Formatted project name
        """

        if '*' in project:
            return Format.red(project)

        return Format.green(project)

    def herd(self,  url: str, ref: Optional[Ref]) -> None:
        """Herd ref

        :param str url: URL of repo
        :param Optional[Ref] ref: Ref to attempt to herd
        """

        is_initial = not self.repo.exists
        if is_initial:
            self.repo.clone(self.path, url, depth=self.depth, ref=ref)
        self.install_project_git_herd_alias()
        if self.config is not None:
            self.repo.update_git_config(self.config)
        if not is_initial:
            self._herd(self.remote, self.default_ref, depth=depth, fetch=fetch, rebase=rebase)

    def herd_branch(self, branch: str) -> None:
        """Herd branch

        :param str branch: Branch name
        """

        if not self.repo.exists:
            self._herd_branch_initial(url, branch, depth=depth)
            self.install_project_git_herd_alias()
            if config is not None:
                self.repo.update_git_config(config)
            return

        if config is not None:
            self.install_project_git_herd_alias()
            self.repo.update_git_config(config)

        if self.repo.has_local_branch(branch):
            self._herd_branch_existing_local(branch, depth=depth, rebase=rebase, upstream_remote=upstream_remote)
            return

        branch_ref = Ref(branch=branch)
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

    def herd_tag(self, tag: str) -> None:
        """Herd tag

        :param str tag: Tag name
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

    def herd_upstream(self) -> None:
        """Herd upstream repo"""

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

        config = {
            'alias.herd': f'!clowder herd {self.repo.path.relative_to(ENVIRONMENT.clowder_dir)}'
        }
        CONSOLE.stdout(" - Update git herd alias")
        self.repo.update_git_config(config)

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

    def _herd(self, remote: str, ref: GitRef, fetch: bool = True, rebase: bool = False) -> None:
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

    # def _herd_branch_initial(self, url: str, branch: str, depth: int = 0) -> None:
    #     """Herd branch initial
    #
    #     :param str url: URL of repo
    #     :param str branch: Branch name to attempt to herd
    #     :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #     """
    #
    #     self._init_repo()
    #     self._create_remote(self.remote, url, remove_dir=True)
    #     self.fetch(self.remote, depth=depth, ref=GitRef(branch=branch))
    #     if not self.has_remote_branch(branch, self.remote):
    #         CONSOLE.stdout(f' - No existing remote branch {fmt.remote(self.remote)} {fmt.ref(branch)}')
    #         self._herd_initial(url, depth=depth)
    #         return
    #     self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)

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

    # def _herd_initial(self, url: str, depth: int = 0) -> None:
    #     """Herd ref initial
    #
    #     :param str url: URL of repo
    #     :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    #     :raise UnknownTypeError:
    #     """
    #
    #     self._init_repo()
    #     self._create_remote(self.remote, url, remove_dir=True)
    #     if self.default_ref.ref_type is GitRefEnum.BRANCH:
    #         self._checkout_new_repo_branch(self.default_ref.short_ref, depth)
    #     elif self.default_ref.ref_type is GitRefEnum.TAG:
    #         self._checkout_new_repo_tag(self.default_ref.short_ref, self.remote, depth, remove_dir=True)
    #     elif self.default_ref.ref_type is GitRefEnum.COMMIT:
    #         self._checkout_new_repo_commit(self.default_ref.short_ref, self.remote, depth)
    #     else:
    #         raise UnknownTypeError('Unknown GitRefEnum type')

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
