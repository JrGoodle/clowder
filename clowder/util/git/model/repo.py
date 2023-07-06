"""Base Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from pygoodle.console import CONSOLE
# from pygoodle.git.decorators import not_detached
from pygoodle.format import Format
from pygoodle.git.constants import GitConfig, HEAD, ORIGIN
from pygoodle.git.decorators import error_msg
from pygoodle.git.log import GIT_LOG
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline

from .branch.local_branch import LocalBranch
from .branch.remote_branch import RemoteBranch
from .branch.tracking_branch import TrackingBranch
from .protocol import Protocol
from .ref import Ref
from .remote import Remote
from .tag.local_tag import LocalTag
from .tag.remote_tag import RemoteTag

if TYPE_CHECKING:
    from .diff import Diff
    from .submodule import Submodule
    from .factory import AllBranches


class Repo:
    """Class encapsulating base git utilities

    :ivar Path path: Absolute path to repo
    :ivar Remote default_remote: Default remote
    """

    def __init__(self, path: Path, default_remote: Optional[str] = None, url: Optional[str] = None,
                 protocol: Protocol = Protocol.SSH):
        """LocalRepo __init__

        :param Path path: Absolute path to repo
        :param str default_remote: Default remote name
        """

        default_remote = ORIGIN if default_remote is None else default_remote

        self.path: Path = path
        self.default_remote: Remote = Remote(self.path, default_remote)
        self.url: Optional[str] = url
        self.protocol: Protocol = protocol

    @property
    def git_dir(self) -> Optional[Path]:
        return GitOffline.git_dir(self.path)

    @error_msg('Failed to clone repo')
    def clone(self, path: Path, url: str, depth: Optional[int] = None, branch: Optional[str] = None,
              jobs: Optional[int] = None, origin: Optional[str] = None) -> 'Repo':
        CONSOLE.stdout(' - Clone repo')
        GitOnline.clone(path, url=url, depth=depth, branch=branch, jobs=jobs, origin=origin)
        return Repo(path)

    @property
    def untracked_files(self) -> List[Path]:
        return GitOffline.get_untracked_files(self.path)

    @property
    def has_untracked_files(self) -> bool:
        return GitOffline.has_untracked_files(self.path)

    @property
    def is_dirty(self) -> bool:
        return GitOffline.is_dirty(self.path)

    @property
    def is_detached(self) -> bool:
        return GitOffline.is_detached(self.path)

    @property
    def is_shallow(self) -> bool:
        return GitOffline.is_shallow_repo(self.path)

    @property
    def is_rebase_in_progress(self) -> bool:
        return GitOffline.is_rebase_in_progress(self.path)

    def get_remotes(self) -> List[Remote]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_remotes(self.path)

    def get_submodules(self) -> List['Submodule']:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_submodules(self.path)

    def get_tracking_branches(self) -> List[TrackingBranch]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_tracking_branches(self.path)

    def get_local_branches(self) -> List[LocalBranch]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_local_branches(self.path)

    def get_remote_branches(self, online: bool = False) -> List[RemoteBranch]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_all_remote_branches(self.path, online=online)

    def get_all_branches(self, online: bool = False) -> 'AllBranches':
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_all_branches(self.path, online=online)

    def has_local_branch(self, branch: str) -> bool:
        local_branch = self.get_local_branch(branch)
        return local_branch is not None

    def has_remote_branch(self, branch: str, remote: Optional[str] = None,
                          url: Optional[str] = None, online: bool = False) -> bool:
        remote_branch = self.get_remote_branch(branch, remote=remote, url=url, online=online)
        return remote_branch is not None

    def has_tracking_branch(self, branch: str, remote: Optional[str] = None) -> bool:
        tracking_branch = self.get_tracking_branch(branch, remote=remote)
        return tracking_branch is not None

    def has_submodule(self, submodule_path: Path) -> bool:
        submodule = self.get_submodule(submodule_path)
        return submodule is not None

    def get_submodule(self, submodule_path: Path) -> Optional['Submodule']:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_submodule(self.path, submodule_path)

    def get_local_branch(self, branch: str) -> Optional[LocalBranch]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_local_branch(self.path, branch)

    def get_remote_branch(self, branch: str, remote: Optional[str] = None,
                          url: Optional[str] = None, online: bool = False) -> Optional[RemoteBranch]:
        remote = ORIGIN if remote is None else remote
        from pygoodle.git.model.factory import GitFactory
        if online or url is not None:
            return GitFactory.get_remote_branch_online(self.path, branch=branch, remote=remote, url=url)
        return GitFactory.get_remote_branch_offline(self.path, branch=branch, remote=remote)

    def get_local_tags(self) -> List[LocalTag]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_local_tags(self.path)

    def get_local_tag(self, tag: str) -> Optional[LocalTag]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_local_tag(self.path, tag)

    def has_local_tag(self, tag: str) -> bool:
        local_tag = self.get_local_tag(tag)
        return local_tag is not None

    def has_remote_tag(self, tag: str, remote: Optional[str] = None,
                       url: Optional[str] = None) -> bool:
        remote_tag = self.get_remote_tag(tag, remote=remote, url=url)
        return remote_tag is not None

    def get_remote_tag(self, tag: str, remote: Optional[str] = None,
                       url: Optional[str] = None) -> Optional[RemoteTag]:
        remote = ORIGIN if remote is None else remote
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_remote_tag(self.path, tag, remote, url=url)

    def get_remote_tags(self, remote: Optional[str] = None,
                        url: Optional[str] = None) -> List[RemoteTag]:
        remote = ORIGIN if remote is None else remote
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_remote_tags(self.path, remote, url=url)

    def get_remote(self, remote: Optional[str] = None, fetch_url: Optional[str] = None,
                   push_url: Optional[str] = None) -> Optional[Remote]:
        from pygoodle.git.model.factory import GitFactory
        remotes = GitFactory.get_remotes(self.path)
        if remote is not None:
            remotes = [r for r in remotes if r.name == remote]
        if fetch_url is not None:
            remotes = [r for r in remotes if r.fetch_url == fetch_url]
        if push_url is not None:
            remotes = [r for r in remotes if r.push_url == push_url]
        return remotes[0] if remotes else None

    def has_remote(self, remote: Optional[str] = None, fetch_url: Optional[str] = None,
                   push_url: Optional[str] = None) -> bool:
        remote = self.get_remote(remote=remote, fetch_url=fetch_url, push_url=push_url)
        return remote is not None

    def get_tracking_branch(self, branch: str, remote: Optional[str] = None) -> Optional[TrackingBranch]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_tracking_branch(self.path, branch, remote=remote)

    def get_diff(self) -> 'Diff':
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_diff(self.path)

    @property
    def exists(self) -> bool:
        return GitOffline.is_repo_cloned(self.path)

    def checkout(self, ref: str, track: bool = False) -> None:
        if self.is_dirty:
            CONSOLE.stdout(' - Dirty repo. Please stash, commit, or discard your changes')
            self.status(verbose=True)
            return
        GitOffline.checkout(self.path, ref=ref, track=track)

    def is_valid(self, allow_missing: bool = True) -> bool:
        """Validate repo state

        :param bool allow_missing: Whether to allow validation to succeed with missing repo
        :return: True, if repo not dirty or doesn't exist on disk
        """

        if not self.exists:
            return allow_missing

        if self.is_dirty or self.is_rebase_in_progress or self.has_untracked_files:
            return False

        submodules = self.get_submodules()
        if not submodules:
            return True
        return all([s.is_valid(allow_missing=allow_missing) for s in submodules])

    def remote(self, name: str) -> Optional[Remote]:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.get_remote(self.path, name)

    @property
    def current_timestamp(self) -> str:
        return GitOffline.current_timestamp(self.path)

    @property
    def current_branch(self) -> str:
        return GitOffline.current_branch(self.path)

    def sha(self, ref: Optional[str] = None, short: bool = False) -> str:
        if ref is None:
            return GitOffline.current_head_commit_sha(self.path, short=short)
        return GitOffline.get_sha(self.path, ref=ref, short=short)

    @error_msg('Failed to abort rebase')
    def abort_rebase(self) -> None:
        if not self.is_rebase_in_progress:
            return
        CONSOLE.stdout(' - Abort rebase in progress')
        GitOffline.abort_rebase(self.path)

    @error_msg('Failed to add files to git index')
    def add(self, files: Union[Path, str, List[str], List[Path]]) -> None:
        if isinstance(files, str):
            files = [files]
        elif isinstance(files, Path):
            files = [str(files)]
        elif isinstance(files, list):
            files = [str(f) for f in files]
        else:
            raise Exception('Wrong type for files parameter')

        CONSOLE.stdout(' - Add files to git index')
        GitOffline.add(self.path, files=files)

    @error_msg('Failed to commit current changes')
    def commit(self, message: str) -> None:
        CONSOLE.stdout(' - Commit current changes')
        GitOffline.commit(self.path, message=message)

    def clean(self, untracked_directories: bool = False, force: bool = False,
              ignored: bool = False, untracked_files: bool = False) -> None:
        """Discard changes for repo

        :param bool untracked_directories: ``d`` Remove untracked directories in addition to untracked files
        :param bool force: ``f`` Delete directories with .git sub directory or file
        :param bool ignored: ``X`` Remove only files ignored by git
        :param bool untracked_files: ``x`` Remove all untracked files
        """

        CONSOLE.stdout(' - Clean repo')
        GitOffline.clean(self.path, untracked_directories=untracked_directories,
                         force=force, ignored=ignored, untracked_files=untracked_files)

    @error_msg('Failed to pull git lfs files')
    def pull_lfs(self) -> None:
        CONSOLE.stdout(' - Pull git lfs files')
        GitOnline.pull_lfs(self.path)

    @error_msg('Failed to reset repo')
    def reset(self, ref: Union[Ref, str] = HEAD, hard: bool = False) -> None:
        if isinstance(ref, TrackingBranch):
            ref = ref.upstream_branch.short_ref
        elif isinstance(ref, Ref):
            ref = ref.short_ref
        CONSOLE.stdout(f' - Reset repo to {Format.Git.ref(ref)}')
        GitOffline.reset(self.path, ref=ref, hard=hard)

    @error_msg('Failed to stash current changes')
    def stash(self) -> None:
        if not self.is_dirty:
            CONSOLE.stdout(' - No changes to stash')
            return
        CONSOLE.stdout(' - Stash current changes')
        GitOffline.stash(self.path)

    def status(self, verbose: bool = False) -> None:
        GitOffline.status(self.path, verbose=verbose)

    @error_msg('Failed to update local git config')
    def update_git_config(self, config: GitConfig) -> None:
        """Update custom git config

        :param GitConfig config: Custom git config
        """

        CONSOLE.stdout(" - Update local git config")
        for key, value in config.items():
            GitOffline.git_config_unset_all_local(self.path, key)
            GitOffline.git_config_add_local(self.path, key, value)

    @error_msg('Failed to update git lfs hooks')
    def install_lfs_hooks(self, local: bool = False) -> None:
        CONSOLE.stdout(' - Update git lfs hooks')
        GitOffline.install_lfs_hooks(self.path, local=local)

    @error_msg('Failed to uninstall git lfs hooks and filters')
    def uninstall_lfs(self) -> None:
        CONSOLE.stdout(' - Uninstall git lfs hooks')
        GitOffline.uninstall_lfs_hooks(self.path)
        CONSOLE.stdout(' - Uninstall git lfs filters')
        GitOffline.uninstall_lfs_filters(self.path)

    @error_msg('Failed to reset timestamp')
    def reset_timestamp(self, timestamp: str, ref: Ref, author: Optional[str] = None) -> None:
        CONSOLE.stdout(' - Reset timestamp')
        GitOffline.reset_timestamp(self.path, timestamp=timestamp, ref=ref.short_ref, author=author)

    def submodule_add(self, url: str, branch: Optional[str] = None, force: bool = False,
                      name: Optional[str] = None, reference: Optional[str] = None, depth: Optional[int] = None,
                      submodule_path: Optional[Path] = None) -> None:
        GitOffline.submodule_add(self.path, url, branch=branch, force=force, name=name,
                                 reference=reference, depth=depth, submodule_path=submodule_path)

    @error_msg('Failed to update submodules')
    def submodule_update(self, init: bool = False, depth: Optional[int] = None, single_branch: bool = False,
                         jobs: Optional[int] = None, recursive: bool = False, remote: bool = False,
                         checkout: bool = False, rebase: bool = False, merge: bool = False,
                         paths: Optional[List[Path]] = None) -> None:
        CONSOLE.stdout(' - Update submodules')
        GitOnline.submodule_update(self.path, init=init, depth=depth, single_branch=single_branch,
                                   jobs=jobs, recursive=recursive, remote=remote, checkout=checkout,
                                   merge=merge, rebase=rebase, paths=paths)

    @error_msg('Failed to deinit submodules')
    def submodule_deinit(self, force: bool = False, paths: Optional[List[Path]] = None) -> None:
        CONSOLE.stdout(' - Deinit submodules')
        GitOffline.submodule_deinit(self.path, force=force, paths=paths)

    @error_msg('Failed to init submodules')
    def submodule_init(self, paths: Optional[List[Path]] = None) -> None:
        CONSOLE.stdout(' - Init submodules')
        GitOffline.submodule_init(self.path, paths=paths)

    @error_msg('Failed to sync submodules')
    def submodule_sync(self, recursive: bool = False, paths: Optional[List[Path]] = None) -> None:
        CONSOLE.stdout(' - Sync submodules')
        GitOffline.submodule_sync(self.path, recursive=recursive, paths=paths)

    def print_local_branches(self) -> None:
        """Print local git branches"""

        for branch in self.get_local_branches():
            if branch.name == self.current_branch:
                CONSOLE.stdout(f'* {Format.green(branch.name)}')
            else:
                CONSOLE.stdout(branch)

    def print_validation(self, allow_missing: bool = False) -> None:
        """Print validation message"""

        if not self.exists or self.is_valid(allow_missing=allow_missing):
            return
        self.status()
        CONSOLE.stdout(f'Dirty repo. Please stash, commit, or discard your changes')

    def groom(self, untracked_directories: bool = True, force: bool = True,
              ignored: bool = False, untracked_files: bool = True) -> None:
        self.clean(untracked_directories=untracked_directories,
                   force=force, ignored=ignored, untracked_files=untracked_files)
        self.reset(hard=True)
        if self.is_rebase_in_progress:
            self.abort_rebase()

    @property
    def formatted_ref(self) -> str:
        """Formatted project repo ref"""

        if self.is_detached:
            return Format.Git.ref(Format.escape(f'[HEAD @ {self.sha()}]'))

        current_branch_output = Format.Git.ref(Format.escape(f'[{self.current_branch}]'))

        local_commits_count = GitOffline.new_commits_count(self.path)
        no_local_commits = local_commits_count == 0
        # TODO: Specify correct remote
        upstream_commits_count = GitOffline.new_commits_count(self.path, upstream=True)
        no_upstream_commits = upstream_commits_count == 0

        if no_local_commits and no_upstream_commits:
            return current_branch_output

        local_commits_output = Format.yellow(f'+{local_commits_count}')
        upstream_commits_output = Format.red(f'-{upstream_commits_count}')
        return f'{current_branch_output}({local_commits_output}/{upstream_commits_output})'

    def print_remote_branches(self) -> None:
        """Print remote git branches"""

        # FIXME: Update this to work
        # Need to get all local, remote, and tracking branches and print them
        # for remote in self.remotes:
        #     for branch in remote.branches:
        #     if ' -> ' in branch:
        #         components = branch.split(' -> ')
        #         local_branch = components[0]
        #         remote_branch = components[1]
        #         CONSOLE.stdout(f"  {Format.red(local_branch)} -> {remote_branch}")
        #     else:
        #         CONSOLE.stdout(Format.red(branch))

    def fetch(self, prune: bool = False, prune_tags: bool = False, tags: bool = False,
              depth: Optional[int] = None, remote: Optional[str] = None, branch: Optional[str] = None,
              unshallow: bool = False, jobs: Optional[int] = None, fetch_all: bool = False, check: bool = True,
              print_output: bool = True):
        # FIXME: Consolidate this implementation with the one for Remotes
        CONSOLE.stdout(f' - Fetch repo')
        try:
            GitOnline.fetch(self.path, remote=remote, prune=prune, prune_tags=prune_tags, tags=tags, depth=depth,
                            branch=branch, unshallow=unshallow, jobs=jobs, fetch_all=fetch_all, print_output=print_output)
        except Exception:  # noqa
            message = f'Failed to fetch repo'
            if check:
                GIT_LOG.error(message)
                raise
            CONSOLE.stdout(message)

    @error_msg('Failed to pull')
    # @not_detached
    def pull(self, remote: Optional[str] = None, branch: Optional[str] = None,
             rebase: bool = False, prune: bool = False, tags: bool = False,
             jobs: Optional[int] = None, no_edit: bool = False, autostash: bool = False,
             depth: Optional[int] = None) -> None:
        # TODO: Check if detached
        message = f' - Pull'
        if rebase:
            message += ' with rebase'
        CONSOLE.stdout(message)
        GitOnline.pull(self.path, remote=remote, branch=branch, rebase=rebase, prune=prune, tags=tags,
                       jobs=jobs, no_edit=no_edit, autostash=autostash, depth=depth)

    # @error_msg('Failed to push')
    # @not_detached
    def push(self, remote: Optional[str] = None, local_branch: Optional[str] = None,
             remote_branch: Optional[str] = None, force: bool = False, set_upstream: bool = False) -> None:
        # TODO: Check if detached
        CONSOLE.stdout(' - Push current branch')
        GitOnline.push(self.path,
                       remote=remote,
                       local_branch=local_branch,
                       remote_branch=remote_branch,
                       force=force,
                       set_upstream=set_upstream)
