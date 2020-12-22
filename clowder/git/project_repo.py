"""Project Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path
from typing import Optional

# import pygoodle.filesystem as fs
# import pygoodle.git as git
from pygoodle.format import Format
from pygoodle.git import (
    Branch,
    Commit,
    LocalBranch,
    Protocol,
    Ref,
    Remote,
    RemoteBranch,
    RemoteTag,
    Repo,
    TrackingBranch
)
from pygoodle.connectivity import is_offline
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import UnknownTypeError
from clowder.data import ResolvedProject
from clowder.data.model import Defaults, Project, Section


def configure_remotes(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        # TODO: Actually configure project and upstream remotes
        # remote_name = self.remote
        # remote_url = self.source.url
        # upstream_remote_name = self.upstream.source.name
        # upstream_remote_url = self.upstream.source.url
        #
        # if not self.exists:
        #     return
        #
        # # FIXME: Find remotes that matchh name or url
        # for remote in self.repo.remotes:
        #     if remote_url == remote.fetch_url and remote.name != remote_name:
        #         remote.rename(remote_name)
        #         continue
        #     if upstream_remote_url == remote.fetch_url and remote.name != upstream_remote_name:
        #         remote.rename(upstream_remote_name)
        # self._compare_remotes(remote_name, remote_url, upstream_remote_name, upstream_remote_url)
        return func(*args, **kwargs)

    return wrapper


# def _compare_remotes(self, remote_name: str, remote_url: str,
#                      upstream_remote_name: str, upstream_remote_url: str) -> None:
#     """Compare remotes names for project and upstream
#
#     :param str remote_name: Project remote name
#     :param str remote_url: Project remote url
#     :param str upstream_remote_name: Upstream remote name
#     :param str upstream_remote_url: Upstream remote url
#     """
#
#     remote_names = [r.name for r in self.repo.remotes]
#     if remote_name in remote_names:
#         self._compare_remote_url(remote_name, remote_url)
#     if upstream_remote_name in remote_names:
#         self._compare_remote_url(upstream_remote_name, upstream_remote_url)


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not Path(instance.full_path / '.git').is_dir():
            CONSOLE.stdout(Format.red('- Project missing'))
            return
        return func(*args, **kwargs)

    return wrapper


class ProjectRepo(ResolvedProject):
    """Class encapsulating git utilities for projects"""

    def __init__(self, project: Project, defaults: Optional[Defaults] = None,
                 section: Optional[Section] = None, protocol: Optional[Protocol] = None):
        """ProjectRepo __init__

        :param Project project: Project model instance
        :param Optional[Defaults] defaults: Defaults instance
        :param Optional[Section] section: Section instance
        """

        super(ProjectRepo, self).__init__(project=project, defaults=defaults, section=section, protocol=protocol)
        remote = Remote(self.full_path, self.remote)
        self.repo: Repo = Repo(self.full_path, remote)

    @property
    def upstream_remote(self) -> Optional[Remote]:
        if self.upstream is None:
            return None
        return Remote(self.full_path, self.upstream.remote)

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        if not is_offline() and remote:
            self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth, ref=self.ref)
            if self.upstream_remote is not None:
                self.upstream_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)

        if local:
            self.repo.print_local_branches()

        if remote:
            if self.upstream:
                CONSOLE.stdout(Format.Git.upstream(self.name))

            self.repo.print_remote_branches()

            if self.upstream:
                CONSOLE.stdout(Format.Git.upstream(self.upstream.name))
                self.upstream.repo.print_remote_branches()

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        branch = Branch(self.full_path, branch)
        branch.checkout(check=False)
        self._pull_lfs()

    @project_repo_exists
    def clean(self, untracked_directories: bool = False, force: bool = False,
              ignored: bool = False, untracked_files: bool = False, submodules: bool = False) -> None:  # noqa
        """Discard changes for repo

        :param bool untracked_directories: ``d`` Remove untracked directories in addition to untracked files
        :param bool force: ``f`` Delete directories with .git sub directory or file
        :param bool ignored: ``X`` Remove only files ignored by git
        :param bool untracked_files: ``x`` Remove all untracked files
        :param bool submodules: Clean submodules recursively
        """

        # FIXME: Need to honor submodules parameter even if recursive is not true
        # self.repo(self.git_settings.recursive or submodules).clean(args=args)
        self.repo.clean(untracked_directories=untracked_directories,
                        force=force,
                        ignored=ignored,
                        untracked_files=untracked_files)
        if submodules:
            raise NotImplementedError

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

    @property
    def current_timestamp(self) -> str:
        """Timestamp of current HEAD commit"""

        return self.repo.current_timestamp

    @project_repo_exists
    def diff(self) -> None:
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        self.repo.status(verbose=True)

    @property
    def exists(self) -> bool:
        """Check if project exists"""

        return self.repo.exists

    @project_repo_exists
    def fetch_all(self) -> None:
        """Fetch upstream changes if project exists on disk"""

        self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)
        if self.upstream is not None:
            self.upstream_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)

    @property
    def formatted_name(self) -> str:
        """Formatted project name"""

        if not self.exists:
            return str(self.path)

        if self.is_dirty:
            return f'{self.path}*'
        else:
            return str(self.path)

    @staticmethod
    def colored_name(name: str) -> str:
        """Return formatted colored project name

        :param str name: Formatted project name
        """

        if '*' in name:
            return Format.red(name)

        return Format.green(name)

    @configure_remotes
    def herd_entrypoint(self, branch: Optional[str] = None, tag: Optional[str] = None,
                        depth: Optional[int] = None, rebase: bool = False) -> None:
        """Clone project or update latest from upstream

        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        herd_depth = self.git_settings.depth if depth is None else depth

        CONSOLE.stdout(self.status())

        if branch:
            self.herd_branch(branch)
        elif tag:
            self.herd_tag(tag)
        else:
            self.herd()

        self._pull_lfs()

        if self.upstream:
            CONSOLE.stdout(Format.Git.upstream(self.upstream.name))
            self.upstream.repo.herd_remote(self.upstream.url, self.upstream.remote, branch=branch)

    def herd(self,  ref: Optional[Ref]) -> None:
        """Herd ref

        :param Optional[Ref] ref: Ref to attempt to herd
        """

        is_initial = not self.exists
        if is_initial:
            self.clone(self.path, url, depth=self.depth, ref=ref)
        self.install_git_herd_alias()
        if self.config is not None:
            self.update_git_config(self.config)
        if not is_initial:
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
            else:
                raise UnknownTypeError('Unknown GitRefEnum type')

    def herd_branch(self, branch: str) -> None:
        """Herd branch

        :param str branch: Branch name
        """

        if not self.exists:
            self._init_repo()
            self._create_remote(self.remote, url, remove_dir=True)
            self.fetch(self.remote, depth=depth, ref=GitRef(branch=branch))
            if not self.has_remote_branch(branch, self.remote):
                CONSOLE.stdout(f' - No existing remote branch {fmt.remote(self.remote)} {Format.Git.ref(branch)}')
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
                return
            self._create_branch_local_tracking(branch, self.remote, depth=depth, fetch=False, remove_dir=True)
            self.install_git_herd_alias()
            if config is not None:
                self.update_git_config(self.config)
            return

        if config is not None:
            self.install_project_git_herd_alias()
            self.update_git_config(self.config)

        if self.has_local_branch(branch):
            self._checkout_branch(branch)

            branch_ref = GitRef(branch=branch)
            self.fetch(self.remote, depth=depth, ref=branch_ref)
            if self.has_remote_branch(branch, self.remote):
                if not self._is_tracking_branch(branch):
                    self._set_tracking_branch_commit(branch, remote, depth)
                    return

                if rebase:
                    self._rebase_remote_branch(remote, branch)
                    return

                self._pull(remote, branch)
                return

            if upstream_remote:
                self.fetch(upstream_remote, depth=depth, ref=branch_ref)
                if self.has_remote_branch(branch, upstream_remote):
                    if not self._is_tracking_branch(branch):
                        self._set_tracking_branch_commit(branch, remote, depth)
                        return

                    if rebase:
                        self._rebase_remote_branch(remote, branch)
                        return

                    self._pull(remote, branch)
            return

        branch_ref = Ref(branch=branch)
        self.fetch(self.remote, depth=depth, ref=branch_ref, allow_failure=True)
        if self.has_remote_branch(branch, self.remote):
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
            else:
                raise UnknownTypeError('Unknown GitRefEnum type')
            return

        CONSOLE.stdout(f' - No existing remote branch {fmt.remote(self.remote)} {Format.Git.ref(branch)}')
        if upstream_remote:
            self.fetch(upstream_remote, depth=depth, ref=branch_ref)
            if self.has_remote_branch(branch, upstream_remote):
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
                else:
                    raise UnknownTypeError('Unknown GitRefEnum type')
                return
            CONSOLE.stdout(f' - No existing remote branch {fmt.remote(upstream_remote)} {Format.Git.ref(branch)}')

        self.herd(url)

    def herd_tag(self, tag: str) -> None:
        """Herd tag

        :param str tag: Tag name
        """

        if not self.exists:
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
            self.update_git_config(config)
        try:
            self.fetch(self.remote, ref=GitRef(tag=tag), depth=depth)
            self._checkout_tag(tag)
        except Exception as err:
            LOG.debug('Failed fetch and checkout tag', err)
            self.herd(url)

    def herd_upstream(self) -> None:
        """Herd upstream repo"""

        if self.upstream is None:
            return

        self.upstream_remote.create(self.upstream.source.url)

        if branch is None:
            self.upstream_remote.fetch(remote, ref=self.default_ref)
            return

        try:
            self.upstream_remote.fetch(remote, ref=GitRef(branch=branch))
        except Exception as err:
            LOG.debug('Failed fetch', err)
            self.upstream_remote.fetch(remote, ref=self.default_ref)

    def install_git_herd_alias(self) -> None:
        """Install 'git herd' alias for project"""

        from clowder.environment import ENVIRONMENT

        config = {
            'alias.herd': f'!clowder herd {self.path.relative_to(ENVIRONMENT.clowder_dir)}'
        }
        CONSOLE.stdout(" - Update git herd alias")
        self.repo.update_git_config(config)

    def is_valid(self, allow_missing: bool = True) -> bool:
        """Validate status of project

        :param bool allow_missing: Whether to allow validation to succeed with missing repo
        :return: True, if not dirty or if the project doesn't exist on disk
        """

        return self.repo.is_valid(allow_missing=allow_missing)

    @property
    def is_dirty(self) -> bool:
        """Check if project is dirty"""

        return not self.repo.is_dirty

    def print_validation(self, allow_missing: bool = True) -> None:
        """Print validation message for project

        :param bool allow_missing: Whether to allow validation to succeed with missing repo
        """

        if not self.is_valid(allow_missing=allow_missing):
            CONSOLE.stdout(self.status())
            self.repo.print_validation()

    @project_repo_exists
    def prune(self, branch: str, force: bool = False,
              local: bool = False, remote: bool = False) -> None:
        """Prune branch

        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        """

        if local:
            local_branch = LocalBranch(self.full_path, branch)
            if local_branch.exists:
                local_branch.delete()

        if remote:
            remote_branch = RemoteBranch(branch, self.repo.default_remote)
            if remote_branch.exists:
                remote_branch.delete()

    def prune_branch_local(self, branch: str, force: bool) -> None:
        """Prune local branch

        :param str branch: Branch name to delete
        :param bool force: Force delete branch
        """

        local_branch = LocalBranch(self.full_path, branch)
        if self.repo.current_branch == local_branch.name:
            self.ref.checkout()
        local_branch.delete()

    def prune_branch_remote(self, branch: str) -> None:
        """Prune remote branch in repository

        :param str branch: Branch name to delete
        """

        remote_branch = RemoteBranch(branch, self.repo.default_remote)
        remote_branch.delete()

    @configure_remotes
    def reset(self, timestamp: Optional[str] = None) -> None:  # noqa
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        """

        # TODO: Restore timestamp author
        # if timestamp:
        #     repo.reset_timestamp(timestamp, self.timestamp_author, self.ref)
        #     self._pull_lfs(repo)
        #     return

        if self.upstream is None:
            self.repo.reset(depth=self.git_settings.depth)
        else:
            CONSOLE.stdout(self.upstream.status())
            CONSOLE.stdout(Format.Git.upstream(self.name))
            self.repo.reset()

        self._pull_lfs()

        self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth, check=False)
        if isinstance(self.ref, TrackingBranch):
            tracking_branch: TrackingBranch = self.ref
            if not tracking_branch.local_branch.exists:
                tracking_branch.local_branch.create()
                return
            tracking_branch.local_branch.checkout()
            if not tracking_branch.upstream_branch.exists:
                raise Exception(f'No existing upstream branch {Format.Git.remote(self.remote)} '
                                f'{Format.Git.ref(tracking_branch.short_ref)}')
            CONSOLE.stdout(f' - Reset branch {Format.Git.ref(tracking_branch.short_ref)} to '
                           f'{Format.Git.remote(self.remote)} {Format.Git.ref(tracking_branch.short_ref)}')
            self.repo.reset(self.ref, hard=True)

    def run(self, command: str, ignore_errors: bool) -> None:
        """Run commands or script in project directory

        :param str command: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        """

        if not self.repo.exists:
            CONSOLE.stdout(Format.red(' - Project missing\n'))
            return

        forall_env = {'CLOWDER_PATH': ENVIRONMENT.clowder_dir,
                      'PROJECT_PATH': self.full_path,
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self.remote,
                      'PROJECT_REF': self.ref.formatted_ref}

        # TODO: Add tests for presence of these variables in test scripts
        # if self.branch:
        #     forall_env['UPSTREAM_BRANCH'] = self.branch
        # if self.tag:
        #     forall_env['UPSTREAM_TAG'] = self.tag
        # if self.commit:
        #     forall_env['UPSTREAM_COMMIT'] = self.commit

        if self.upstream:
            forall_env['UPSTREAM_REMOTE'] = self.upstream.remote
            forall_env['UPSTREAM_NAME'] = self.upstream.name
            forall_env['UPSTREAM_REF'] = self.upstream.ref.formatted_ref

        self._run_forall_command(command, forall_env, ignore_errors)

    def sha(self, short: bool = False) -> str:
        """Return sha for currently checked out commit

        :param bool short: Whether to return short or long commit sha
        :return: Commit sha
        """

        return self.repo.current_commit(short=short).short_ref

    @project_repo_exists
    def start(self, branch: str, tracking: bool) -> None:
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        depth = self.git_settings.depth

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
            CONSOLE.stdout(f' - {Format.Git.ref(branch)} already exists')
            if self._is_branch_checked_out(branch):
                CONSOLE.stdout(' - On correct branch')
            else:
                self._checkout_branch_local(branch)

        if tracking and not is_offline():
            self._create_branch_remote_tracking(branch, remote, depth)

    def status(self, padding: Optional[int] = None) -> str:
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        """

        if not self.repo.exists:
            project_output = self.name
            if padding:
                project_output = project_output.ljust(padding)
                project_output = Format.green(project_output)
                missing_output = Format.red('-')
                return f'{project_output} {missing_output}'
            project_output = Format.green(project_output)
            return project_output

        project_output = self.formatted_name
        if padding:
            project_output = project_output.ljust(padding)
        project_output = self.colored_name(project_output)
        return f'{project_output} {self.repo.formatted_ref}'

    @project_repo_exists
    def stash(self) -> None:
        """Stash changes for project if dirty"""

        self.repo.stash()

    def _pull_lfs(self) -> None:
        """Pull lfs files"""

        if not self.git_settings.lfs:
            return

        self.repo.install_lfs_hooks()
        self.repo.pull_lfs()
