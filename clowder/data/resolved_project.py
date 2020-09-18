# -*- coding: utf-8 -*-
"""Representation of clowder yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path
from typing import List, Optional, Set

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git_project import ProjectRepo, ProjectRepoRecursive
from clowder.git_project.util import (
    existing_git_repository,
    git_url
)
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_forall_command

from .resolved_git_settings import ResolvedGitSettings
from .resolved_upstream import ResolvedUpstream
from .source_controller import SOURCE_CONTROLLER, GITHUB
from .model import Defaults, Project, Source, Group


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not Path(instance.full_path() / '.git').is_dir():
            cprint(" - Project missing", 'red')
            return
        return func(*args, **kwargs)

    return wrapper


class ResolvedProject:
    """clowder yaml Project model class

    :ivar str name: Project name
    :ivar Path path: Project relative path
    :ivar Set[str] groups: Groups project belongs to
    :ivar str remote: Project remote name
    :ivar Source source: Project source
    :ivar ResolvedGitSettings git_settings: Custom git settings
    :ivar Optional[ResolvedUpstream] upstream: Project's associated upstream
    :ivar Optional[str] default_protocol: Protocol defined in defaults
    :ivar str ref: Project git ref
    :ivar Optional[str] default_protocol: Default git protocol to use
    """

    def __init__(self, project: Project, defaults: Optional[Defaults] = None,
                 group: Optional[Group] = None, protocol: Optional[str] = None):
        """Project __init__

        :param Project project: Project model instance
        :param Optional[Defaults] defaults: Defaults instance
        :param Optional[Group] group: Group instance
        """

        project.resolved_project_id = id(self)
        self.name: str = project.name
        self._print_output = True

        has_path = project.path is not None
        has_defaults = defaults is not None
        has_group = group is not None
        has_group_defaults = has_group and group.defaults is not None

        has_group_path = has_group and group.path is not None
        self.path: Path = Path()
        if has_group_path:
            self.path = self.path / group.path
        if has_path:
            self.path = self.path / project.path
        else:
            last_path_component = Path(self.name).name
            self.path = self.path / last_path_component

        has_group_protocol = has_group and group.protocol is not None
        self.default_protocol: Optional[str] = None
        if has_group_protocol:
            self.default_protocol: Optional[str] = group.protocol
        elif protocol is not None:
            self.default_protocol: Optional[str] = protocol

        has_remote = project.remote is not None
        has_defaults_remote = has_defaults and defaults.remote is not None
        has_group_defaults_remote = has_group_defaults and group.defaults.remote is not None
        self.remote: str = "origin"
        if has_remote:
            self.remote = project.remote
        elif has_group_defaults_remote:
            self.remote = group.defaults.remote
        elif has_defaults_remote:
            self.remote = defaults.remote

        has_source = project.source is not None
        has_defaults_source = has_defaults and defaults.source is not None
        has_group_defaults_source = has_group_defaults and group.defaults.source is not None
        self.source: Source = SOURCE_CONTROLLER.get_source(GITHUB)
        if has_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(project.source)
        elif has_group_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(group.defaults.source)
        elif has_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(defaults.source)

        has_ref = project.get_formatted_ref() is not None
        has_defaults_ref = has_defaults and defaults.get_formatted_ref() is not None
        has_group_defaults_ref = has_group_defaults and group.defaults.get_formatted_ref() is not None
        self.ref: str = "refs/heads/master"
        if has_ref:
            self.ref = project.get_formatted_ref()
        elif has_group_defaults_ref:
            self.ref = group.defaults.get_formatted_ref()
        elif has_defaults_ref:
            self.ref = defaults.get_formatted_ref()

        has_git = project.git_settings is not None
        has_defaults_git = has_defaults and defaults.git_settings is not None
        has_group_defaults_git = has_group_defaults and group.defaults.git_settings is not None
        self.git_settings: ResolvedGitSettings = ResolvedGitSettings()
        if has_defaults_git:
            self.git_settings.update(defaults.git_settings)
        if has_group_defaults_git:
            self.git_settings.update(group.defaults.git_settings)
        if has_git:
            self.git_settings.update(project.git_settings)

        self.upstream: Optional[ResolvedUpstream] = None
        if project.upstream is not None:
            self.upstream: Optional[ResolvedUpstream] = ResolvedUpstream(self.path, project.upstream,
                                                                         defaults, group, protocol)
            if self.remote == self.upstream.remote:
                message = fmt.error_remote_dup(self.upstream.name,  self.name, self.remote, ENVIRONMENT.clowder_yaml)
                err = ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_REMOTE_NAME, message)
                LOG_DEBUG('Duplicate remote name found in clowder.yml', err)
                raise err

        self.groups: Set[str] = {"all", self.name, str(self.path)}
        if has_group:
            self.groups.add(group.name)
            if group.groups is not None:
                self.groups.update({g for g in group.groups})
        if project.groups is not None:
            self.groups.update(set(project.groups))
        if 'notdefault' in self.groups:
            self.groups.remove('all')

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)

        if not is_offline() and remote:
            if self.upstream is None:
                repo.fetch(self.remote, depth=self.git_settings.depth)
            else:
                repo.fetch(self.upstream.remote)
                repo.fetch(self.remote)

        if self.upstream is None:
            if local:
                repo.print_local_branches()
            if remote:
                repo.print_remote_branches()
            return

        if local:
            repo.print_local_branches()
        if remote:
            self._print(fmt.upstream_string(self.name))
            repo.print_remote_branches()

            self._print(fmt.upstream_string(self.upstream.name))
            # Modify repo to prefer upstream
            repo.default_ref = self.upstream.ref
            repo.remote = self.upstream.remote
            repo.print_remote_branches()
            # Restore repo configuration
            repo.default_ref = self.ref
            repo.remote = self.remote

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        repo = self._repo(self.git_settings.recursive)
        repo.checkout(branch, allow_failure=True)
        self._pull_lfs(repo)

    @project_repo_exists
    def clean(self, args: str = '', submodules: bool = False) -> None:
        """Discard changes for project

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param bool submodules: Clean submodules recursively
        """

        self._repo(self.git_settings.recursive or submodules).clean(args=args)

    @project_repo_exists
    def clean_all(self) -> None:
        """Discard all changes for project

        Equivalent to:
        ``git clean -ffdx; git reset --hard; git rebase --abort``
        ``git submodule foreach --recursive git clean -ffdx``
        ``git submodule foreach --recursive git reset --hard``
        ``git submodule update --checkout --recursive --force``
        """

        self._repo(self.git_settings.recursive).clean(args='fdx')

    @project_repo_exists
    def diff(self) -> None:
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        self._repo(self.git_settings.recursive).status_verbose()

    def existing_branch(self, branch: str, is_remote: bool) -> bool:
        """Check if branch exists

        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if branch exists
        :rtype: bool
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        if not is_remote:
            return repo.existing_local_branch(branch)

        return repo.existing_remote_branch(branch, self.remote)

    def exists(self) -> bool:
        """Check if branch exists

        :return: True, if repo exists
        :rtype: bool
        """

        return existing_git_repository(self.full_path())

    @project_repo_exists
    def fetch_all(self) -> None:
        """Fetch upstream changes if project exists on disk"""

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        if self.upstream is None:
            repo.fetch(self.remote, depth=self.git_settings.depth)
            return

        repo.fetch(self.upstream.remote)
        repo.fetch(self.remote)

    def formatted_project_output(self) -> str:
        """Return formatted project path/name

        :return: Formatted string of full file path if cloned, otherwise project name
        :rtype: str
        """

        if existing_git_repository(self.full_path()):
            return colored(str(self.path), 'green')

        return colored(self.name, 'green')

    def full_path(self) -> Path:
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return ENVIRONMENT.clowder_dir / self.path

    def get_current_timestamp(self) -> str:
        """Return timestamp of current HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return repo.get_current_timestamp()

    def herd(self, branch: Optional[str] = None, tag: Optional[str] = None, depth: Optional[int] = None,
             rebase: bool = False, parallel: bool = False) -> None:
        """Clone project or update latest from upstream

        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param bool parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        herd_depth = self.git_settings.depth if depth is None else depth
        repo = self._repo(self.git_settings.recursive, parallel=parallel)

        if self.upstream is None:
            self._print(self.status())

            if branch:
                repo.herd_branch(self._url(), branch, depth=herd_depth,
                                 rebase=rebase, config=self.git_settings.get_processed_config())
            elif tag:
                repo.herd_tag(self._url(), tag, depth=herd_depth, rebase=rebase,
                              config=self.git_settings.get_processed_config())
            else:
                repo.herd(self._url(), depth=herd_depth, rebase=rebase,
                          config=self.git_settings.get_processed_config())
            self._pull_lfs(repo)

            return

        self._print(self.status())
        repo.configure_remotes(self.remote, self._url(), self.upstream.remote, self.upstream.url())

        # self._print(fmt.upstream_string(self.name))
        if branch:
            repo.herd_branch(self._url(), branch, depth=herd_depth, rebase=rebase,
                             config=self.git_settings.get_processed_config())
        elif tag:
            repo.herd_tag(self._url(), tag, depth=herd_depth, rebase=rebase,
                          config=self.git_settings.get_processed_config())
        else:
            repo.herd(self._url(), depth=herd_depth, rebase=rebase,
                      config=self.git_settings.get_processed_config())

        self._pull_lfs(repo)

        self._print(fmt.upstream_string(self.upstream.name))

        # Modify repo to prefer upstream
        repo.default_ref = self.upstream.ref
        repo.remote = self.upstream.remote
        repo.herd_remote(self.upstream.url(), self.upstream.remote, branch=branch)
        # Restore repo configuration
        repo.default_ref = self.ref
        repo.remote = self.remote

    def is_dirty(self) -> bool:
        """Check if project is dirty

        :return: True, if dirty
        :rtype: bool
        """

        return not self._repo(self.git_settings.recursive).validate_repo()

    def is_valid(self, allow_missing_repo: bool = True) -> bool:
        """Validate status of project

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        :return: True, if not dirty or if the project doesn't exist on disk
        :rtype: bool
        """

        return ProjectRepo(self.full_path(), self.remote, self.ref).validate_repo(allow_missing_repo=allow_missing_repo)

    def print_existence_message(self) -> None:
        """Print existence validation message for project"""

        if not existing_git_repository(self.full_path()):
            print(self.status())

    def print_validation(self, allow_missing_repo: bool = True) -> None:
        """Print validation message for project

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        """

        if not self.is_valid(allow_missing_repo=allow_missing_repo):
            print(self.status())
            repo = ProjectRepo(self.full_path(), self.remote, self.ref)
            repo.print_validation()

    @project_repo_exists
    def prune(self, branch: str, force: bool = False,
              local: bool = False, remote: bool = False) -> None:
        """Prune branch

        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)

        if local and repo.existing_local_branch(branch):
            repo.prune_branch_local(branch, force)

        if remote:
            if repo.existing_remote_branch(branch, self.remote):
                repo.prune_branch_remote(branch, self.remote)

    def reset(self, timestamp: Optional[str] = None, parallel: bool = False) -> None:
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        :param bool parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        repo = self._repo(self.git_settings.recursive, parallel=parallel)

        # TODO: Restore timestamp author
        # if timestamp:
        #     repo.reset_timestamp(timestamp, self.timestamp_author, self.ref)
        #     self._pull_lfs(repo)
        #     return

        if self.upstream is None:
            repo.reset(depth=self.git_settings.depth)
        else:
            self._print(self.upstream.status())
            repo.configure_remotes(self.remote, self._url(), self.upstream.remote, self.upstream.url())
            self._print(fmt.upstream_string(self.name))
            repo.reset()

        self._pull_lfs(repo)

    def run(self, commands: List[str], ignore_errors: bool, parallel: bool = False) -> None:
        """Run commands or script in project directory

        :param list[str] commands: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param bool parallel: Whether commands are being run in parallel, affects output
        """

        if not parallel and not existing_git_repository(self.full_path()):
            print(colored(" - Project missing\n", 'red'))
            return

        self._print_output = not parallel

        forall_env = {'CLOWDER_PATH': ENVIRONMENT.clowder_dir,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self.remote,
                      'PROJECT_REF': self.ref}

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
            forall_env['UPSTREAM_REF'] = self.upstream.ref

        for cmd in commands:
            self._run_forall_command(cmd, forall_env, ignore_errors)

    def sha(self, short: bool = False) -> str:
        """Return sha for currently checked out commit

        :param bool short: Whether to return short or long commit sha
        :return: Commit sha
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return repo.sha(short=short)

    @project_repo_exists
    def start(self, branch: str, tracking: bool) -> None:
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        # TODO: Replace 0 with git default depth
        depth = self.git_settings.depth
        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        repo.start(self.remote, branch, depth, tracking)

    def status(self, padding: Optional[int] = None) -> str:
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        :rtype: str
        """

        if not existing_git_repository(self.full_path()):
            project_output = colored(self.name, 'green')
            if padding:
                project_output = project_output.ljust(padding)
                missing_output = colored('-', 'red')
                return f'{project_output} {missing_output}'
            return project_output

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        project_output = repo.format_project_string(self.path)
        current_ref_output = repo.format_project_ref_string()

        if padding:
            project_output = project_output.ljust(padding)

        return f'{project_output} {current_ref_output}'

    @project_repo_exists
    def stash(self) -> None:
        """Stash changes for project if dirty"""

        if self.is_dirty():
            repo = ProjectRepo(self.full_path(), self.remote, self.ref)
            repo.stash()
        else:
            print(" - No changes to stash")

    def _pull_lfs(self, repo: ProjectRepo) -> None:
        """Check if git lfs is installed and if not install them

        :param ProjectRepo repo: Repo object
        """

        if not self.git_settings.lfs:
            return

        repo.install_lfs_hooks()
        repo.pull_lfs()

    def _print(self, val: str) -> None:
        """Print output if self._print_output is True

        :param str val: String to print
        """

        if self._print_output:
            print(val)

    # FIXME: Turn this into a property
    def _repo(self, submodules: bool, parallel: bool = False) -> ProjectRepo:
        """Return ProjectRepo or ProjectRepoRecursive instance

        :param bool submodules: Whether to handle submodules
        :param bool parallel: Whether command is being run in parallel

        :return: Project repo instance
        :rtype: ProjectRepo
        """

        if submodules:
            return ProjectRepoRecursive(self.full_path(), self.remote, self.ref, parallel=parallel)
        return ProjectRepo(self.full_path(), self.remote, self.ref, parallel=parallel)

    def _run_forall_command(self, command: str, env: dict, ignore_errors: bool) -> None:
        """Run command or script in project directory

        :param str command: Command to run
        :param dict env: Environment variables
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :raise ClowderError:
        """

        self._print(fmt.command(command))
        try:
            execute_forall_command(command, self.full_path(), env, self._print_output)
        except ClowderError as err:
            LOG_DEBUG('Execute command failed', err)
            if not ignore_errors:
                raise

    def _url(self) -> str:
        """Return project url"""

        if self.source.protocol is not None:
            protocol = self.source.protocol
        elif SOURCE_CONTROLLER.protocol_override is not None:
            protocol = SOURCE_CONTROLLER.protocol_override
        elif self.default_protocol is not None:
            protocol = self.default_protocol
        else:
            protocol = SOURCE_CONTROLLER.get_default_protocol()

        return git_url(protocol, self.source.url, self.name)
