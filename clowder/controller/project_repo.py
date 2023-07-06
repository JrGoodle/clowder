"""Project Git utility class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path
from typing import Optional

import clowder.util.filesystem as fs
from clowder.util.format import Format
from clowder.util.git import (
    Branch,
    LocalBranch,
    Protocol,
    Remote,
    RemoteBranch,
    RemoteTag,
    Repo,
    TrackingBranch
)
from clowder.util.connectivity import is_offline
from clowder.util.console import CONSOLE

from clowder.environment import ENVIRONMENT
from clowder.model import Defaults, Project, Section

from .resolved_project import ResolvedProject


def configure_remotes(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        # TODO: Actually configure project and upstream remotes
        # remote_name = self.remote
        # remote_url = self.url
        # upstream_remote_name = self.upstream.source.name
        # upstream_remote_url = self.upstream.url
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
        if not Path(instance.path / '.git').is_dir():
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
        self.repo: Repo = Repo(self.path, self.default_remote.name)

        if self.default_branch is None and self.default_tag is None and self.default_commit is None:
            remote_branch = self.repo.default_remote.default_branch(self.url)
            if remote_branch is None:
                remote_branch = RemoteBranch(self.path, 'master', remote=self.default_remote.name)
            self.default_branch = TrackingBranch(self.path,
                                                 local_branch=remote_branch.name,
                                                 upstream_remote=remote_branch.remote.name)

    @property
    def upstream_remote(self) -> Optional[Remote]:
        if self.upstream is None:
            return None
        return Remote(self.path, self.upstream.remote.name)

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        if not is_offline() and remote:
            self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth,
                                           branch=self.default_ref.short_ref)
            if self.upstream_remote is not None:
                self.upstream_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)

        if local:
            self.repo.print_local_branches()

        if remote:
            if self.upstream:
                CONSOLE.stdout(Format.Git.upstream(self.name))

            self.repo.print_remote_branches()
            # TODO: Move this into pygoodle
            if self.upstream:
                CONSOLE.stdout(Format.Git.upstream(self.upstream.name))
                # self.upstream_remote.print_branches()

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        branch = Branch(self.path, branch)
        branch.checkout(check=False)
        if self.git_settings.lfs:
            self.repo.install_lfs_hooks()
            self.repo.pull_lfs()

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
        # TODO: Move this to 'groom' command
        self.repo.reset(hard=True)
        if self.repo.is_rebase_in_progress:
            self.repo.abort_rebase()
        if submodules:
            raise NotImplementedError

    @project_repo_exists
    def diff(self) -> None:
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        self.repo.status(verbose=True)

    @project_repo_exists
    def fetch(self) -> None:
        """Fetch upstream changes if project exists on disk"""

        self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)
        if self.upstream is not None:
            self.upstream_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth)

    @configure_remotes
    def herd(self, branch: Optional[str] = None, tag: Optional[str] = None,
             depth: Optional[int] = None, rebase: bool = False) -> None:
        """Clone project or update latest from upstream

        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        depth = self.git_settings.depth if depth is None else depth

        CONSOLE.stdout(self.status())
        is_initial_clone = False
        if not self.repo.exists:
            is_initial_clone = True
            if self.path.exists() and fs.has_contents(self.path):
                raise Exception('Non-empty directory already exists')
            fs.remove_dir(self.path, ignore_errors=True)

            clone_branch = None if self.default_branch is None else self.default_branch.short_ref
            if branch is not None:
                remote_branch = RemoteBranch(self.path, name=branch, remote=self.default_remote.name)
                if remote_branch.exists_online(self.url):
                    clone_branch = branch

            self.repo.clone(self.path, url=self.url, depth=depth, branch=clone_branch, origin=self.default_remote.name)

            if tag is not None:
                remote_tag = RemoteTag(self.path, name=tag, remote=self.default_remote.name)
                if remote_tag.exists:
                    remote_tag.checkout()
            elif self.default_tag is not None:
                self.default_tag.checkout()
            elif self.default_commit is not None:
                self.default_commit.checkout()

        self.install_git_herd_alias()
        if self.git_settings is not None and self.git_settings.config is not None:
            self.repo.update_git_config(self.git_settings.config)

        if not is_initial_clone:
            if not self.default_remote.exists:
                self.default_remote.create(self.url, fetch=True, tags=True)

            if self.default_branch is not None:
                self.herd_branch(self.default_branch, check=True, create=True, rebase=rebase)
            elif self.default_tag is not None:
                self.default_tag.checkout()
            elif self.default_commit is not None:
                self.default_commit.checkout()

            if branch is not None:
                tracking_branch = TrackingBranch(self.path,
                                                 local_branch=branch,
                                                 upstream_branch=branch,
                                                 upstream_remote=self.default_remote.name)
                self.herd_branch(tracking_branch, check=False, create=False, rebase=rebase)
            elif tag is not None:
                remote_tag = RemoteTag(self.path, tag, self.default_remote.name)
                if remote_tag.exists:
                    remote_tag.checkout()

        if self.git_settings.lfs:
            self.repo.install_lfs_hooks(local=True)
            self.repo.pull_lfs()

        if self.upstream is not None:
            CONSOLE.stdout(Format.Git.upstream(self.upstream.name))
            if not self.upstream_remote.exists:
                self.upstream_remote.create(self.upstream.url)
            self.upstream_remote.fetch(prune=True, tags=True)

        if self.git_settings.recursive:
            self.repo.submodule_update(init=True, depth=self.git_settings.depth, recursive=True, checkout=True)

    @staticmethod
    def herd_branch(branch: TrackingBranch, check: bool = True, create: bool = True,
                    rebase: bool = False) -> None:
        if not branch.local_branch.exists:
            if branch.upstream_branch.exists:
                branch.upstream_branch.checkout(check=check, track=True)
            elif create:
                branch.local_branch.create()
            return

        # local branch exists
        if not branch.upstream_branch.exists or not branch.is_checked_out:
            branch.local_branch.checkout(check=check)

        # local and remote branches exist
        if not branch.is_tracking_branch:
            branch.set_upstream()

        branch.upstream_branch.pull(rebase=rebase, no_edit=True)

    def install_git_herd_alias(self) -> None:
        """Install 'git herd' alias for project"""

        # TODO: Check if already installed and exit early
        config = {
            'alias.herd': f'!clowder herd {self.relative_path}'
        }
        CONSOLE.stdout(f" - Update {Format.bold('git herd')} alias")
        self.repo.update_git_config(config)

    @project_repo_exists
    def prune(self, branch: str, force: bool = False,
              local: bool = False, remote: bool = False) -> None:
        """Prune branch

        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        """

        if self.repo.current_branch == branch and local:
            self.checkout(self.default_ref.formatted_ref)

        if local:
            local_branch = LocalBranch(self.path, branch)
            if local_branch.exists:
                local_branch.delete(force=force)

        if remote:
            remote_branch = RemoteBranch(self.path, branch, self.repo.default_remote.name)
            if remote_branch.exists:
                remote_branch.delete()

    def prune_branch_local(self, branch: str, force: bool) -> None:
        """Prune local branch

        :param str branch: Branch name to delete
        :param bool force: Force delete branch
        """

        local_branch = LocalBranch(self.path, branch)
        if self.repo.current_branch == local_branch.name:
            self.default_ref.checkout()
        local_branch.delete(force=force)

    def prune_branch_remote(self, branch: str) -> None:
        """Prune remote branch in repository

        :param str branch: Branch name to delete
        """

        remote_branch = RemoteBranch(self.path, branch, self.repo.default_remote.name)
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

        # if self.upstream is None:
        #     self.repo.reset(hard=True)
        # else:
        #     # FIXME: Print correct status
        #     # CONSOLE.stdout(self.upstream.status())
        #     CONSOLE.stdout(Format.Git.upstream(self.name))
        #     self.repo.reset(hard=True)

        self.repo.default_remote.fetch(prune=True, tags=True, depth=self.git_settings.depth, check=False)
        if self.default_branch is not None:
            if not self.default_branch.local_branch.exists:
                self.default_branch.local_branch.create()
                return
            self.default_branch.local_branch.checkout()
            if not self.default_branch.upstream_branch.exists:
                raise Exception(f'No existing upstream branch {Format.Git.remote(self.default_remote.name)} '
                                f'{Format.Git.ref(self.default_branch.short_ref)}')
            CONSOLE.stdout(f' - Reset branch {Format.Git.ref(self.default_branch.short_ref)} to '
                           f'{Format.Git.remote(self.default_branch.upstream_branch.remote.name)} '
                           f'{Format.Git.ref(self.default_branch.short_ref)}')
            self.repo.reset(self.default_ref, hard=True)

        if self.git_settings.lfs:
            self.repo.install_lfs_hooks()
            self.repo.pull_lfs()

    def run(self, command: str, check: bool) -> None:
        """Run commands or script in project directory

        :param str command: Commands to run
        :param bool check: Whether to exit if command returns a non-zero exit code
        """

        if not self.repo.exists:
            CONSOLE.stdout(Format.red(' - Project missing\n'))
            return

        forall_env = {
            'CLOWDER_PATH': ENVIRONMENT.clowder_dir,
            'PROJECT_PATH': self.path,
            'PROJECT_NAME': self.name,
            'PROJECT_REMOTE': self.default_remote.name,
            'PROJECT_REF': self.default_ref.formatted_ref
        }

        if self.upstream:
            forall_env['UPSTREAM_REMOTE'] = self.upstream.remote.name
            forall_env['UPSTREAM_NAME'] = self.upstream.name

        self._run_forall_command(command, forall_env, check=check)

    @project_repo_exists
    def start(self, branch: str, tracking: bool) -> None:
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        local_branch = LocalBranch(self.path, branch)

        if not local_branch.exists:
            local_branch.create(track=False)

        if local_branch.is_checked_out:
            CONSOLE.stdout(f' - On correct branch {Format.Git.ref(local_branch.name)}')
        else:
            local_branch.checkout()

        if not tracking:
            return

        self.repo.fetch(prune=True)
        tracking_branch = TrackingBranch(self.path,
                                         local_branch=branch,
                                         upstream_branch=branch,
                                         upstream_remote=self.default_remote.name)
        tracking_branch.create()

    def formatted_name(self, padding: Optional[int] = None, color: bool = False) -> str:
        """Formatted project name"""

        if not self.repo.exists:
            output = str(self.relative_path)
        else:
            if self.repo.is_dirty:
                output = f'{self.name}*'
            else:
                output = self.name

        if padding is not None:
            output = output.ljust(padding)

        if not color:
            return output

        if '*' in output:
            return Format.red(output)
        return Format.green(output)

    def status(self, padding: Optional[int] = None) -> str:
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        """

        output = self.formatted_name(padding=padding, color=True)
        if not self.repo.exists:
            if padding is None:
                return output
            else:
                return f"{output} {Format.red('-')}"

        return f'{output} {self.repo.formatted_ref}'

        # FIXME: Also print upstream if it exists
        # if not existing_git_repo(self.path):
        #     return Format.green(self.path)
        #
        # repo = ProjectRepo(self.path, self.remote, self.ref)
        # project_output = repo.format_project_string(self.path)
        # return f"{project_output} {repo.formatted_ref}"

    @project_repo_exists
    def stash(self) -> None:
        """Stash changes for project if dirty"""

        self.repo.stash()
