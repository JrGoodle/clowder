"""Representation of clowder yaml project

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Optional, Set

from pygoodle.connectivity import is_offline
from pygoodle.console import CONSOLE
from pygoodle.formatting import Format

import clowder.util.formatting as fmt
from clowder.app import LOG
from clowder.environment import ENVIRONMENT
from clowder.git import (
    GitProtocol,
    GitRef,
    ProjectRepo,
    ProjectRepoRecursive
)
from clowder.git.util import existing_git_repo
from clowder.util.error import DuplicateRemoteError
from clowder.util.execute import execute_forall_command

from .resolved_git_settings import ResolvedGitSettings
from .resolved_upstream import ResolvedUpstream
from .source_controller import SOURCE_CONTROLLER, GITHUB
from .model import Defaults, Project, Source, Section


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not Path(instance.full_path / '.git').is_dir():
            CONSOLE.stdout(Format.red("- Project missing"))
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
    :ivar Optional[str] ref: Project git ref
    :ivar Optional[GitProtocol] default_protocol: Default git protocol to use
    """

    def __init__(self, project: Project, defaults: Optional[Defaults] = None,
                 section: Optional[Section] = None, protocol: Optional[GitProtocol] = None):
        """Project __init__

        :param Project project: Project model instance
        :param Optional[Defaults] defaults: Defaults instance
        :param Optional[Section] section: Section instance
        :raise DuplicateRemoteError:
        """

        self._repo: Optional[ProjectRepo] = None
        project.resolved_project_id = id(self)
        self.name: str = project.name

        has_path = project.path is not None
        has_section = section is not None
        has_group_path = has_section and section.path is not None
        self.path: Path = section.path if has_group_path else Path()
        if has_path:
            self.path: Path = self.path / project.path
        else:
            self.path: Path = self.path / Path(self.name).name

        self.remote: str = self._get_property('remote', project, defaults, section, default='origin')
        self.ref: Optional[GitRef] = self._get_property('git_ref', project, defaults, section)
        self.git_settings: ResolvedGitSettings = ResolvedGitSettings.combine_settings(project, section, defaults)

        source = self._get_property('source', project, defaults, section, default=GITHUB)
        self.source: Source = SOURCE_CONTROLLER.get_source(source)

        self.default_protocol: Optional[GitProtocol] = None
        if self.source.protocol is not None:
            self.default_protocol: Optional[GitProtocol] = self.source.protocol
        elif protocol is not None:
            self.default_protocol: Optional[GitProtocol] = protocol

        self.upstream: Optional[ResolvedUpstream] = None
        if project.upstream is not None:
            self.upstream: Optional[ResolvedUpstream] = ResolvedUpstream(self.path, project.upstream,
                                                                         defaults, section, protocol)
            if self.remote == self.upstream.remote:
                message = f"{fmt.invalid_yaml(ENVIRONMENT.clowder_yaml.name)}\n" \
                          f"{fmt.path(ENVIRONMENT.clowder_yaml)}\n" \
                          f"upstream '{self.upstream.name}' and project '{self.name}' " \
                          f"have same remote name '{self.remote}'"
                raise DuplicateRemoteError(message)

        self.groups: Set[str] = {'all', self.name, str(self.path)}
        if has_section:
            self.groups.add(section.name)
            if section.groups is not None:
                self.groups.update({g for g in section.groups})
        if project.groups is not None:
            self.groups.update(set(project.groups))
        if 'notdefault' in self.groups:
            self.groups.remove('all')

    @property
    def full_path(self) -> Path:
        """Full path to project"""

        return ENVIRONMENT.clowder_dir / self.path

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        if not is_offline() and remote:
            self.repo.fetch(self.remote, depth=self.git_settings.depth)
            if self.upstream:
                self.repo.fetch(self.upstream.remote)

        if local:
            self.repo.print_local_branches()

        if remote:
            if self.upstream:
                CONSOLE.stdout(fmt.upstream(self.name))

            self.repo.print_remote_branches()

            if self.upstream:
                CONSOLE.stdout(fmt.upstream(self.upstream.name))
                self.upstream.repo.print_remote_branches()

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        self.repo.checkout(branch, allow_failure=True)
        self._pull_lfs()

    @project_repo_exists
    def clean(self, args: str = '', submodules: bool = False) -> None:  # noqa
        """Discard changes for project

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param bool submodules: Clean submodules recursively
        """

        # FIXME: Need to honor submodules parameter even if recursive is not true
        # self.repo(self.git_settings.recursive or submodules).clean(args=args)
        self.repo.clean(args=args)

    @project_repo_exists
    def clean_all(self) -> None:
        """Discard all changes for project

        Equivalent to:
        ``git clean -ffdx; git reset --hard; git rebase --abort``
        ``git submodule foreach --recursive git clean -ffdx``
        ``git submodule foreach --recursive git reset --hard``
        ``git submodule update --checkout --recursive --force``
        """

        self.repo.clean(args='fdx')

    @project_repo_exists
    def diff(self) -> None:
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        self.repo.status_verbose()

    def has_branch(self, branch: str, is_remote: bool) -> bool:
        """Check if branch exists

        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if branch exists
        """

        if not is_remote:
            return self.repo.has_local_branch(branch)

        return self.repo.has_remote_branch(branch, self.remote)

    def exists(self) -> bool:
        """Check if project exists

        :return: True, if repo exists
        """

        return existing_git_repo(self.full_path)

    @project_repo_exists
    def fetch_all(self) -> None:
        """Fetch upstream changes if project exists on disk"""

        if self.upstream is None:
            self.repo.fetch(self.remote, depth=self.git_settings.depth)
            return

        self.repo.fetch(self.upstream.remote)
        self.repo.fetch(self.remote)

    def formatted_project_output(self) -> str:
        """Return formatted project path/name

        :return: Formatted string of full file path if cloned, otherwise project name
        """

        if existing_git_repo(self.full_path):
            return str(self.path)

        return self.name

    @property
    def current_timestamp(self) -> str:
        """Timestamp of current HEAD commit"""

        return self.repo.current_timestamp

    def herd(self, branch: Optional[str] = None, tag: Optional[str] = None, depth: Optional[int] = None,
             rebase: bool = False) -> None:
        """Clone project or update latest from upstream

        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        herd_depth = self.git_settings.depth if depth is None else depth

        CONSOLE.stdout(self.status())

        if self.upstream:
            self.repo.configure_remotes(self.remote, self.url,
                                        self.upstream.remote, self.upstream.url)

        if branch:
            self.repo.herd_branch(self.url, branch, depth=herd_depth, rebase=rebase,
                                  config=self.git_settings.get_processed_config())
        elif tag:
            self.repo.herd_tag(self.url, tag, depth=herd_depth, rebase=rebase,
                               config=self.git_settings.get_processed_config())
        else:
            self.repo.herd(self.url, depth=herd_depth, rebase=rebase,
                           config=self.git_settings.get_processed_config())

        self._pull_lfs()

        if self.upstream:
            CONSOLE.stdout(fmt.upstream(self.upstream.name))
            self.upstream.repo.herd_remote(self.upstream.url, self.upstream.remote, branch=branch)

    @property
    def is_dirty(self) -> bool:
        """Check if project is dirty"""

        return not self.repo.validate_repo()

    def is_valid(self, allow_missing_repo: bool = True) -> bool:
        """Validate status of project

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        :return: True, if not dirty or if the project doesn't exist on disk
        """

        return self.repo.validate_repo(allow_missing_repo=allow_missing_repo)

    def print_existence_message(self) -> None:
        """Print existence validation message for project"""

        if not existing_git_repo(self.full_path):
            CONSOLE.stdout(self.status())

    def print_validation(self, allow_missing_repo: bool = True) -> None:
        """Print validation message for project

        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        """

        if not self.is_valid(allow_missing_repo=allow_missing_repo):
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

        if local and self.repo.has_local_branch(branch):
            self.repo.prune_branch_local(branch, force)

        if remote:
            if self.repo.has_remote_branch(branch, self.remote):
                self.repo.prune_branch_remote(branch, self.remote)

    @property
    def repo(self) -> ProjectRepo:
        """ProjectRepo or ProjectRepoRecursive instance"""

        if self._repo is not None:
            return self._repo

        if self.git_settings.recursive:
            return ProjectRepoRecursive(self.full_path, self.remote, self.ref)
        else:
            return ProjectRepo(self.full_path, self.remote, self.ref)

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
            self.repo.configure_remotes(self.remote, self.url, self.upstream.remote, self.upstream.url)
            CONSOLE.stdout(fmt.upstream(self.name))
            self.repo.reset()

        self._pull_lfs()

    def run(self, command: str, ignore_errors: bool) -> None:
        """Run commands or script in project directory

        :param str command: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        """

        if not existing_git_repo(self.full_path):
            CONSOLE.stdout(Format.red(" - Project missing\n"))
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

        return self.repo.sha(short=short)

    @project_repo_exists
    def start(self, branch: str, tracking: bool) -> None:
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        depth = self.git_settings.depth
        self.repo.start(self.remote, branch, depth, tracking)

    def status(self, padding: Optional[int] = None) -> str:
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        """

        if not existing_git_repo(self.full_path):
            project_output = self.name
            if padding:
                project_output = project_output.ljust(padding)
                project_output = Format.green(project_output)
                missing_output = Format.red('-')
                return f'{project_output} {missing_output}'
            project_output = Format.green(project_output)
            return project_output

        project_output = self.repo.format_project_string(self.path)
        if padding:
            project_output = project_output.ljust(padding)
        project_output = self.repo.color_project_string(project_output)
        return f'{project_output} {self.repo.formatted_ref}'

    @project_repo_exists
    def stash(self) -> None:
        """Stash changes for project if dirty"""

        if self.is_dirty:
            self.repo.stash()
        else:
            CONSOLE.stdout(" - No changes to stash")

    def update_default_branch(self, branch: str) -> None:
        """Update ref with default branch if none set"""

        if self.ref is None:
            self.ref = GitRef(branch=branch)

    @property
    def url(self) -> str:
        """Project url"""

        if self.source.protocol is not None:
            protocol = self.source.protocol
        elif SOURCE_CONTROLLER.protocol_override is not None:
            protocol = SOURCE_CONTROLLER.protocol_override
        elif self.default_protocol is not None:
            protocol = self.default_protocol
        else:
            protocol = SOURCE_CONTROLLER.get_default_protocol()

        return protocol.format_url(self.source.url, self.name)

    def _pull_lfs(self) -> None:
        """Pull lfs files"""

        if not self.git_settings.lfs:
            return

        self.repo.install_lfs_hooks()
        self.repo.pull_lfs()

    def _run_forall_command(self, command: str, env: dict, ignore_errors: bool) -> None:
        """Run command or script in project directory

        :param str command: Command to run
        :param dict env: Environment variables
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        """

        CONSOLE.stdout(fmt.command(command))
        try:
            execute_forall_command(command, self.full_path, env)
        except CalledProcessError as err:
            if ignore_errors:
                LOG.debug(f'Command failed: {command}', err)
            else:
                LOG.error(f'Command failed: {command}')
                raise

    @staticmethod
    def _get_property(name: str, project: Project, defaults: Optional[Defaults], section: Optional[Section],
                      default: Optional[Any] = None) -> Optional[Any]:
        project_value = getattr(project, name)
        has_defaults = defaults is not None
        defaults_value = getattr(defaults, name) if has_defaults else None
        has_section = section is not None
        has_section_defaults = has_section and section.defaults is not None
        section_defaults_value = getattr(section.defaults, name) if has_section_defaults else None
        if project_value is not None:
            return project_value
        elif section_defaults_value is not None:
            return section_defaults_value
        elif defaults_value is not None:
            return defaults_value
        elif default is not None:
            return default
        else:
            return None
