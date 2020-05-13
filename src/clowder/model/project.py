# -*- coding: utf-8 -*-
"""Representation of clowder.yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from functools import wraps
from typing import List, Optional

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_exit import ClowderExit
from clowder.git.project_repo import ProjectRepo
from clowder.git.project_repo_recursive import ProjectRepoRecursive
from clowder.git.util import (
    existing_git_repository,
    git_url
)
from clowder.model.defaults import Defaults
from clowder.model.fork import Fork
from clowder.model.source import Source
from clowder.util.execute import execute_forall_command


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not os.path.isdir(os.path.join(instance.full_path(), '.git')):
            cprint(" - Project repo is missing", 'red')
            return
        return func(*args, **kwargs)

    return wrapper


class Project(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar List[str] groups: Groups project belongs to
    :ivar str ref: Project git ref
    :ivar str remote: Project remote name
    :ivar int depth: Depth to clone project repo
    :ivar bool recursive: Whether to recursively clone submodules
    :ivar Source source: Default source
    :ivar Optional[Fork] fork: Project's associated Fork
    """

    def __init__(self, project: dict, defaults: Defaults, sources: List[Source]):
        """Project __init__

        :param dict project: Parsed YAML python object for project
        :param Defaults defaults: Defaults instance
        :param List[Source] sources: List of Source instances
        :raise ClowderYAMLError:
        """

        self.name = project['name']
        self.path = project.get('path', self.name)
        self.ref = project.get('ref', defaults.ref)
        self.remote = project.get('remote', defaults.remote)
        self.depth = project.get('depth', defaults.depth)
        self.recursive = project.get('recursive', defaults.recursive)
        self._timestamp_author = project.get('timestamp_author', defaults.timestamp_author)
        self._print_output = True

        groups = [self.name, 'all']
        custom_groups = project.get('groups', None)
        if custom_groups:
            groups += custom_groups
        if 'notdefault' in groups:
            groups.remove('all')
        self.groups = list(set(groups))

        self.source = None
        source_name = project.get('source', defaults.source)
        for source in sources:
            if source.name == source_name:
                self.source = source

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            self.fork = Fork(fork, self.path, self.name, self.source, sources, self.ref, self.recursive, defaults)

    @project_repo_exists
    def branch(self, local: bool = False, remote: bool = False) -> None:
        """Print branches for project

        :param bool local: Print local branches
        :param bool remote: Print remote branches
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        # TODO: Rethink aggressively fetching for printing remote branches
        # if not is_offline() and remote:
        #     if self.fork is None:
        #         repo.fetch(self.remote, depth=self.depth)
        #     else:
        #         repo.fetch(self.fork.remote)
        #         repo.fetch(self.remote)

        repo.print_branches(local=local, remote=remote)

    @project_repo_exists
    def checkout(self, branch: str) -> None:
        """Checkout branch

        :param str branch: Branch to check out
        """

        self._repo(self.recursive).checkout(branch, allow_failure=True)

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

        self._repo(self.recursive or recursive).clean(args=args)

    @project_repo_exists
    def clean_all(self) -> None:
        """Discard all changes for project

        Equivalent to:
        ``git clean -ffdx; git reset --hard; git rebase --abort``
        ``git submodule foreach --recursive git clean -ffdx``
        ``git submodule foreach --recursive git reset --hard``
        ``git submodule update --checkout --recursive --force``
        """

        self._repo(self.recursive).clean(args='fdx')

    @project_repo_exists
    def diff(self) -> None:
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        self._repo(self.recursive).status_verbose()

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
            repo.fetch(self.remote, depth=self.depth)
            return

        repo.fetch(self.fork.remote)
        repo.fetch(self.remote)

    def formatted_project_path(self) -> str:
        """Return formatted project path

        :return: Formatted string of full file path
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return repo.format_project_string(self.path)

    def full_path(self) -> str:
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(ROOT_DIR, self.path)

    def get_current_timestamp(self) -> str:
        """Return timestamp of current HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return repo.get_current_timestamp()

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation for saving yaml

        :param bool resolved: Return default ref rather than current commit sha
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            ref = self.ref
        else:
            if self.fork is None:
                ref = self.ref
            else:
                repo = ProjectRepo(self.full_path(), self.remote, self.ref)
                ref = repo.sha()

        project = {'name': self.name,
                   'path': self.path,
                   'groups': self.groups,
                   'depth': self.depth,
                   'recursive': self.recursive,
                   'ref': ref,
                   'remote': self.remote,
                   'source': self.source.name}

        if self.fork:
            fork_yaml = self.fork.get_yaml()
            project['fork'] = fork_yaml

        if self._timestamp_author:
            project['timestamp_author'] = self._timestamp_author

        return project

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

        herd_depth = self.depth if depth is None else depth
        repo = self._repo(self.recursive, parallel=parallel)

        if self.fork is None:
            if branch:
                repo.herd_branch(self._url(), branch, depth=herd_depth, rebase=rebase)
            elif tag:
                repo.herd_tag(self._url(), tag, depth=herd_depth, rebase=rebase)
            else:
                repo.herd(self._url(), depth=herd_depth, rebase=rebase)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(), self.fork.remote, self.fork.url())

        self._print(fmt.fork_string(self.name))
        # Modify repo to prefer fork
        repo.default_ref = self.fork.ref
        repo.remote = self.fork.remote
        if branch:
            repo.herd_branch(self.fork.url(), branch, depth=herd_depth, rebase=rebase)
        elif tag:
            repo.herd_tag(self.fork.url(), tag, depth=herd_depth, rebase=rebase)
        else:
            repo.herd(self.fork.url(), depth=herd_depth, rebase=rebase)

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

        return not self._repo(self.recursive).validate_repo()

    def is_valid(self) -> bool:
        """Validate status of project

        :return: True, if not dirty or if the project doesn't exist on disk
        :rtype: bool
        """

        return ProjectRepo(self.full_path(), self.remote, self.ref).validate_repo()

    def print_existence_message(self) -> None:
        """Print existence validation message for project"""

        if not existing_git_repository(self.full_path()):
            print(self.status())

    def print_validation(self) -> None:
        """Print validation message for project"""

        if not self.is_valid():
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

        repo = self._repo(self.recursive, parallel=parallel)

        if self.fork is None:
            if timestamp:
                repo.reset_timestamp(timestamp, self._timestamp_author, self.ref)
                return

            repo.reset(depth=self.depth)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(), self.fork.remote, self.fork.url())

        self._print(fmt.fork_string(self.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self._timestamp_author, self.ref)
            return

        repo.reset()

    def run(self, commands: List[str], ignore_errors: bool, parallel: bool = False) -> None:
        """Run commands or script in project directory

        :param list[str] commands: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param bool parallel: Whether commands are being run in parallel, affects output
        """

        if not parallel and not existing_git_repository(self.full_path()):
            print(colored(" - Project is missing\n", 'red'))
            return

        self._print_output = not parallel

        forall_env = {'CLOWDER_PATH': ROOT_DIR,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self.remote,
                      'PROJECT_REF': self.ref}

        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote
            forall_env['FORK_NAME'] = self.fork.name
            forall_env['FORK_REF'] = self.fork.ref

        for cmd in commands:
            self._run_forall_command(cmd, forall_env, ignore_errors, parallel)

    @project_repo_exists
    def start(self, branch: str, tracking: bool) -> None:
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        remote = self.remote if self.fork is None else self.fork.remote
        depth = self.depth if self.fork is None else 0
        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        repo.start(remote, branch, depth, tracking)

    def status(self, padding: Optional[int] = None) -> str:
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        :rtype: str
        """

        if not existing_git_repository(self.full_path()):
            return colored(self.name, 'green')

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

    def sync(self, rebase: bool = False, parallel: bool = False) -> None:
        """Sync fork project with upstream remote

        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param bool parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        self.herd(rebase=rebase, parallel=parallel)
        self._print(self.fork.status())
        repo = self._repo(self.recursive, parallel=parallel)
        repo.sync(self.fork.remote, rebase=rebase)

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

    def _run_forall_command(self, command: str, env: dict, ignore_errors: bool, parallel: bool) -> None:
        """Run command or script in project directory

        :param str command: Command to run
        :param dict env: Environment variables
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param bool parallel: Whether command is being run in parallel, affects output

        Raises:
            ClowderError
            ClowderExit
        """

        self._print(fmt.command(command))
        try:
            execute_forall_command(command, self.full_path(), env, self._print_output)
        except ClowderError:
            if not ignore_errors:
                err = fmt.error_command_failed(command)
                self._print(err)
                if parallel:
                    raise ClowderError(err)
                raise ClowderExit(1)

    def _url(self) -> str:
        """Return project url"""

        return git_url(self.source.protocol, self.source.url, self.name)
