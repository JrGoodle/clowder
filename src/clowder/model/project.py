# -*- coding: utf-8 -*-
"""Representation of clowder yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from functools import wraps
from pathlib import Path
from typing import List, Optional, Tuple

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git import ProjectRepo, ProjectRepoRecursive
from clowder.git.util import (
    existing_git_repository,
    format_git_branch,
    format_git_tag,
    git_url
)
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_forall_command

from .defaults import Defaults
from .fork import Fork, ForkImpl
from .git_settings import GitSettings, GitSettingsImpl
from .source import Source


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


class ProjectImpl(object):
    """clowder yaml Project model impl class

    :ivar str name: Project name
    """

    def __init__(self, project: dict):
        """Project __init__

        :param dict project: Parsed YAML python object for project
        """

        self.name: str = project['name']
        self._path: Optional[str] = project.get('path', None)
        self._remote: Optional[str] = project.get('remote', None)
        self._source: Optional[str] = project.get('source', None)
        self._branch: Optional[str] = project.get("branch", None)
        self._tag: Optional[str] = project.get("tag", None)
        self._commit: Optional[str] = project.get("commit", None)
        self._groups: Optional[List[str]] = project.get('groups', None)
        self._timestamp_author: Optional[str] = project.get('timestamp_author', None)

        git_settings = project.get("git", None)
        if git_settings is not None:
            self._git_settings = GitSettingsImpl(git_settings)
        else:
            self._git_settings = None

        fork = project.get('fork', None)
        if fork is not None:
            self._fork = ForkImpl(fork)
        else:
            self._fork = None

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        project = {'name': self.name}

        if self._path is not None:
            project['path'] = self._path
        if self._remote is not None:
            project['remote'] = self._remote
        if self._source is not None:
            project['source'] = self._source
        if self._groups is not None:
            project['groups'] = self._groups
        if self._fork is not None:
            project['fork'] = self._fork.get_yaml(resolved_sha=resolved_sha)
        if self._git_settings is not None:
            project['git'] = self._git_settings.get_yaml()
        if self._timestamp_author is not None:
            project['timestamp_author'] = self._timestamp_author

        if resolved_sha is None:
            if self._branch is not None:
                project['branch'] = self._branch
            elif self._tag is not None:
                project['tag'] = self._tag
            elif self._commit is not None:
                project['commit'] = self._commit
        else:
            project['commit'] = resolved_sha

        return project


class Project(ProjectImpl):
    """clowder yaml Project model class

    :ivar Path path: Project relative path
    :ivar List[str] groups: Groups project belongs to
    :ivar str ref: Project git ref
    :ivar str remote: Project remote name
    :ivar Source source: Default source
    :ivar GitSettings git_settings: Custom git settings
    :ivar Optional[Fork] fork: Project's associated Fork
    """

    def __init__(self, project: dict, defaults: Defaults, sources: Tuple[Source, ...]):
        """Project __init__

        :param dict project: Parsed YAML python object for project
        :param Defaults defaults: Defaults instance
        :param Tuple[Source, ...] sources: List of Source instances
        """

        super().__init__(project)

        self.path: Path = Path(project.get('path', Path(self.name).name))
        self.remote: str = project.get('remote', defaults.remote)
        self.timestamp_author: Optional[str] = project.get('timestamp_author', defaults.timestamp_author)

        self._print_output = True

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self.ref = defaults.ref

        git_settings = project.get("git", None)
        if git_settings is not None:
            self.git_settings = GitSettings(git_settings=git_settings, default_git_settings=defaults.git_settings)
        else:
            self.git_settings = defaults.git_settings

        self.source = None
        source_name = project.get('source', defaults.source)
        for source in sources:
            if source.name == source_name:
                self.source = source
                break
        if self.source is None:
            message = fmt.error_source_not_found(source_name, ENVIRONMENT.clowder_yaml, self.name)
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            self.fork = Fork(fork, self, sources, defaults)
            if self.remote == self.fork.remote:
                message = fmt.error_remote_dup(self.fork.name, self.name, self.remote, ENVIRONMENT.clowder_yaml)
                raise ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_REMOTE_NAME, message)

        groups = ['all', self.name, str(self.path)]
        if self._groups is not None:
            groups += copy.deepcopy(self._groups)
        if self.fork is not None:
            groups += [self.fork.name]
        groups = list(set(groups))
        if 'notdefault' in groups:
            groups.remove('all')
        self.groups = groups

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)

        if not is_offline() and remote:
            if self.fork is None:
                repo.fetch(self.remote, depth=self.git_settings.depth)
            else:
                repo.fetch(self.fork.remote)
                repo.fetch(self.remote)

        if self.fork is None:
            if local:
                repo.print_local_branches()
            if remote:
                repo.print_remote_branches()
            return

        if local:
            repo.print_local_branches()
        if remote:
            self._print(fmt.fork_string(self.fork.name))
            # Modify repo to prefer fork
            repo.default_ref = self.fork.ref
            repo.remote = self.fork.remote
            repo.print_remote_branches()

            self._print(fmt.fork_string(self.name))
            # Restore repo configuration
            repo.default_ref = self.ref
            repo.remote = self.remote
            repo.print_remote_branches()

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        repo = self._repo(self.git_settings.recursive)
        repo.checkout(branch, allow_failure=True)
        self._pull_lfs(repo)

    @project_repo_exists
    def clean(self, args: str = '', recursive: bool = False) -> None:
        """Discard changes for project

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param bool recursive: Clean submodules recursively
        """

        self._repo(self.git_settings.recursive or recursive).clean(args=args)

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

        remote = self.remote if self.fork is None else self.fork.remote
        return repo.existing_remote_branch(branch, remote)

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
        if self.fork is None:
            repo.fetch(self.remote, depth=self.git_settings.depth)
            return

        repo.fetch(self.fork.remote)
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

        if self.fork is None:
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

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(), self.fork.remote, self.fork.url())

        self._print(fmt.fork_string(self.fork.name))
        # Modify repo to prefer fork
        repo.default_ref = self.fork.ref
        repo.remote = self.fork.remote
        if branch:
            repo.herd_branch(self.fork.url(), branch, depth=herd_depth, rebase=rebase,
                             config=self.git_settings.get_processed_config())
        elif tag:
            repo.herd_tag(self.fork.url(), tag, depth=herd_depth, rebase=rebase,
                          config=self.git_settings.get_processed_config())
        else:
            repo.herd(self.fork.url(), depth=herd_depth, rebase=rebase,
                      config=self.git_settings.get_processed_config())
        self._pull_lfs(repo)

        self._print(fmt.fork_string(self.name))
        # Restore repo configuration
        repo.default_ref = self.ref
        repo.remote = self.remote
        repo.herd_remote(self._url(), self.remote, branch=branch)

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
            if self.fork:
                # Modify repo to prefer fork
                repo.default_ref = self.fork.ref
                repo.remote = self.fork.remote
            repo.prune_branch_local(branch, force)

        if remote:
            git_remote = self.remote if self.fork is None else self.fork.remote
            if repo.existing_remote_branch(branch, git_remote):
                repo.prune_branch_remote(branch, git_remote)

    def reset(self, timestamp: Optional[str] = None, parallel: bool = False) -> None:
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        :param bool parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        repo = self._repo(self.git_settings.recursive, parallel=parallel)

        if self.fork is None:
            if timestamp:
                repo.reset_timestamp(timestamp, self.timestamp_author, self.ref)
                self._pull_lfs(repo)
                return

            repo.reset(depth=self.git_settings.depth)
            self._pull_lfs(repo)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(), self.fork.remote, self.fork.url())

        self._print(fmt.fork_string(self.fork.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self.timestamp_author, self.ref)
            self._pull_lfs(repo)
            return

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
        if self._branch:
            forall_env['PROJECT_BRANCH'] = self._branch
        if self._tag:
            forall_env['PROJECT_TAG'] = self._tag
        if self._commit:
            forall_env['PROJECT_COMMIT'] = self._commit

        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote
            forall_env['FORK_NAME'] = self.fork.name
            forall_env['FORK_REF'] = self.fork.ref

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

        remote = self.remote if self.fork is None else self.fork.remote
        depth = self.git_settings.depth if self.fork is None else GitSettings.depth
        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        repo.start(remote, branch, depth, tracking)

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

    def _repo(self, recursive: bool, parallel: bool = False) -> ProjectRepo:
        """Return ProjectRepo or ProjectRepoRecursive instance

        :param bool recursive: Whether to handle submodules
        :param bool parallel: Whether command is being run in parallel

        :return: Project repo instance
        :rtype: ProjectRepo
        """

        if recursive:
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

        return git_url(self.source.protocol.value, self.source.url, self.name)
