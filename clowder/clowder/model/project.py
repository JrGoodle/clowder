# -*- coding: utf-8 -*-
"""Representation of clowder.yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import inspect
import os

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.git.project_repo import ProjectRepo
from clowder.git.project_repo_recursive import ProjectRepoRecursive
from clowder.git.util import (
    existing_git_repository,
    format_project_ref_string,
    format_project_string,
    git_url,
    print_validation
)
from clowder.model.fork import Fork
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_forall_command


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

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
    :ivar str ref: Default git ref
    :ivar str remote: Default remote name
    :ivar int depth: Depth to clone project repo
    :ivar bool recursive: Whether to recursively clone submodules
    :ivar Source source: Default source
    :ivar Fork fork: Project's associated Fork
    """

    def __init__(self, project, group, defaults, sources):
        """Project __init__

        :param dict project: Parsed YAML python object for project
        :param dict group: Parsed YAML python object for group
        :param Defaults defaults: Defaults instance
        :param list[Source] sources: List of Source instances
        :raise ClowderYAMLError:
        """

        self.name = project['name']
        self.path = project['path']

        self.ref = project.get('ref', group.get('ref', defaults.ref))
        self.remote = project.get('remote', group.get('remote', defaults.remote))
        self.depth = project.get('depth', group.get('depth', defaults.depth))
        self.recursive = project.get('recursive', group.get('recursive', defaults.recursive))
        self._protocol = defaults.protocol
        self._timestamp_author = project.get('timestamp_author',
                                             group.get('timestamp_author', defaults.timestamp_author))
        self._print_output = True

        self.source = None
        source_name = project.get('source', group.get('source', defaults.source))
        for source in sources:
            if source.name == source_name:
                self.source = source

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            if fork['remote'] == self.remote:
                raise ClowderYAMLError(fmt.remote_name_error(fork['name'], self.name, self.remote))
            self.fork = Fork(fork, self.path, self.source, self._protocol)

    @project_repo_exists
    def branch(self, local=False, remote=False):
        """Print branches for project

        .. py:function:: branch(local=False, remote=False)

        :param Optional[bool] local: Print local branches
        :param Optional[bool] remote: Print remote branches
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        if not is_offline() and remote:
            if self.fork is None:
                repo.fetch(self.remote, depth=self.depth)
            else:
                repo.fetch(self.fork.remote_name)
                repo.fetch(self.remote)

        repo.print_branches(local=local, remote=remote)

    @project_repo_exists
    def checkout(self, branch):
        """Checkout branch

        :param str branch: Branch to check out
        """

        self._repo(self.full_path(), self.remote, self.ref, self.recursive).checkout(branch, allow_failure=True)

    @project_repo_exists
    def clean(self, args='', recursive=False):
        """Discard changes for project

        .. py:function:: clean(args='', recursive=False)

        :param Optional[str] args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param Optional[bool] recursive: Clean submodules recursively
        """

        self._repo(self.full_path(), self.remote, self.ref, self.recursive and recursive).clean(args=args)

    @project_repo_exists
    def clean_all(self):
        """Discard all changes for project

        Equivalent to:
        ``git clean -ffdx; git reset --hard; git rebase --abort``
        ``git submodule foreach --recursive git clean -ffdx``
        ``git submodule foreach --recursive git reset --hard``
        ``git submodule update --checkout --recursive --force``
        """

        self._repo(self.full_path(), self.remote, self.ref, self.recursive).clean(args='fdx')

    @project_repo_exists
    def diff(self):
        """Show git diff for project

        Equivalent to: ``git status -vv``
        """

        ProjectRepo(self.full_path(), self.remote, self.ref).status_verbose()

    def existing_branch(self, branch, is_remote):
        """Check if branch exists

        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if branch exists
        :rtype: bool
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        if not is_remote:
            return repo.existing_local_branch(branch)

        remote = self.remote if self.fork is None else self.fork.remote_name
        return repo.existing_remote_branch(branch, remote)

    @project_repo_exists
    def fetch_all(self):
        """Fetch upstream changes if project exists on disk"""

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        if self.fork is None:
            repo.fetch(self.remote, depth=self.depth)
            return

        repo.fetch(self.fork.remote_name)
        repo.fetch(self.remote)

    def formatted_project_path(self):
        """Return formatted project path

        :return: Formatted string of full file path
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return format_project_string(repo, self.path)

    def full_path(self):
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(ROOT_DIR, self.path)

    def get_current_timestamp(self):
        """Return timestamp of current HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        return repo.get_current_timestamp()

    def get_yaml(self, resolved=False):
        """Return python object representation for saving yaml

        .. py:function:: get_yaml(resolved=False)

        :param Optional[bool] resolved: Return default ref rather than current commit sha
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            ref = self.ref
        else:
            repo = ProjectRepo(self.full_path(), self.remote, self.ref)
            ref = repo.sha()

        project = {'name': self.name,
                   'path': self.path,
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

    def herd(self, **kwargs):
        """Clone project or update latest from upstream

        .. py:function:: herd(branch=None, tag=None, depth=0, rebase=False, parallel=False)

        Keyword Args:
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
            parallel (bool): Whether command is being run in parallel, affects output
            protocol (str): Git protocol ('ssh' or 'https')
        """

        branch = kwargs.get('branch', None)
        tag = kwargs.get('tag', None)
        depth = kwargs.get('depth', None)
        rebase = kwargs.get('rebase', False)
        parallel = kwargs.get('parallel', False)
        protocol = kwargs.get('protocol', self._protocol)

        self._print_output = not parallel

        herd_depth = self.depth if depth is None else depth
        repo = self._repo(self.full_path(), self.remote, self.ref, self.recursive, parallel=parallel)

        if branch:
            fork_remote = None if self.fork is None else self.fork.remote_name
            self._run_herd_command('herd_branch', repo, protocol, branch,
                                   depth=herd_depth, rebase=rebase, fork_remote=fork_remote)
            return

        if tag:
            self._run_herd_command('herd_tag', repo, protocol, tag, depth=herd_depth, rebase=rebase)
            return

        self._run_herd_command('herd', repo, protocol, depth=herd_depth, rebase=rebase)

    def is_dirty(self):
        """Check if project is dirty

        :return: True, if dirty
        :rtype: bool
        """

        return not self._repo(self.full_path(), self.remote, self.ref, self.recursive).validate_repo()

    def is_valid(self):
        """Validate status of project

        :return: True, if not dirty or if the project doesn't exist on disk
        :rtype: bool
        """

        return ProjectRepo(self.full_path(), self.remote, self.ref).validate_repo()

    def print_validation(self):
        """Print validation message for project"""

        if not self.is_valid():
            print(self.status())
            repo = ProjectRepo(self.full_path(), self.remote, self.ref)
            print_validation(repo)

    @project_repo_exists
    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branch

        .. py:function:: prune(branch, force=False, local=False, remote=False)

        :param str branch: Branch to prune
        :param Optional[bool] force: Force delete branch
        :param Optional[bool] local: Delete local branch
        :param Optional[bool] remote: Delete remote branch
        """

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)

        if local and repo.existing_local_branch(branch):
            repo.prune_branch_local(branch, force)

        if remote:
            git_remote = self.remote if self.fork is None else self.fork.remote_name
            if repo.existing_remote_branch(branch, git_remote):
                repo.prune_branch_remote(branch, git_remote)

    def reset(self, timestamp=None, parallel=False):
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        .. py:function:: reset(timestamp=None, parallel=False)

        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        repo = self._repo(self.full_path(), self.remote, self.ref, self.recursive, parallel=parallel)

        if self.fork is None:
            if timestamp:
                repo.reset_timestamp(timestamp, self._timestamp_author, self.ref)
                return

            repo.reset(depth=self.depth)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(), self.fork.remote_name, self.fork.url(self._protocol))

        self._print(fmt.fork_string(self.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self._timestamp_author, self.ref)
            return

        repo.reset()

    def run(self, commands, ignore_errors, parallel=False):
        """Run commands or script in project directory

        .. py:function:: run(commands, ignore_errors, parallel=False)

        :param list[str] commands: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param Optional[bool] parallel: Whether commands are being run in parallel, affects output
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
            forall_env['FORK_REMOTE'] = self.fork.remote_name

        for cmd in commands:
            self._run_forall_command(cmd, forall_env, ignore_errors, parallel)

    @project_repo_exists
    def start(self, branch, tracking):
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        """

        remote = self.remote if self.fork is None else self.fork.remote_name
        depth = self.depth if self.fork is None else 0
        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        repo.start(remote, branch, depth, tracking)

    def status(self, padding=None):
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        :rtype: str
        """

        if not existing_git_repository(self.full_path()):
            return colored(self.name, 'green')

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        project_output = format_project_string(repo, self.path)
        current_ref_output = format_project_ref_string(repo)

        if padding:
            project_output = project_output.ljust(padding)

        return project_output + ' ' + current_ref_output

    @project_repo_exists
    def stash(self):
        """Stash changes for project if dirty"""

        if self.is_dirty():
            repo = ProjectRepo(self.full_path(), self.remote, self.ref)
            repo.stash()

    def sync(self, protocol, rebase=False, parallel=False):
        """Sync fork project with upstream remote

        .. py:function:: sync(rebase=False, parallel=False)

        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output
        """

        self._print_output = not parallel

        if protocol is None:
            protocol = self._protocol

        repo = self._repo(self.full_path(), self.remote, self.ref, self.recursive, parallel=parallel)
        self._run_herd_command('herd', repo, protocol, rebase=rebase)
        self._print(self.fork.status())
        repo.sync(self.fork.remote_name, rebase=rebase)

    def _print(self, val):
        """Print output if self._print_output is True

        :param str val: String to print
        """

        if self._print_output:
            print(val)

    @staticmethod
    def _repo(path, remote, ref, recursive, **kwargs):
        """Return ProjectRepo or ProjectRepoRecursive instance

        :param str path: Repo path
        :param str remote: Default repo remote
        :param str ref: Default repo ref
        :param bool recursive: Whether to handle submodules

        Keyword Args:
            parallel (bool): Whether command is being run in parallel
            print_output (bool): Whether to print output
        """

        if recursive:
            return ProjectRepoRecursive(path, remote, ref, **kwargs)
        return ProjectRepo(path, remote, ref, **kwargs)

    def _run_forall_command(self, command, env, ignore_errors, parallel):
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
                err = fmt.command_failed_error(command)
                self._print(err)
                if parallel:
                    raise ClowderError(err)
                raise ClowderExit(1)

    def _run_herd_command(self, command, repo, protocol, *args, **kwargs):
        """Run herd command

        :param str command: Repo path
        :param ProjectRepo repo: ProjectRepo or ProjectRepoRecursive instance
        :param str protocol: Git protocol ('ssh' or 'https')

        Other Parameters:
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
            fork_remote (str): Fork remote name
        """

        if self.fork is None:
            getattr(repo, command)(self._url(protocol), *args, **kwargs)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self.remote, self._url(protocol), self.fork.remote_name, self.fork.url(protocol))

        self._print(fmt.fork_string(self.name))
        kwargs['depth'] = 0
        getattr(repo, command)(self._url(protocol), *args, **kwargs)

        self._print(fmt.fork_string(self.fork.name))

        frame = inspect.currentframe()
        vals = inspect.getargvalues(frame)
        branch_arg = [a for a in vals.args if vals.locals[a] if vals.locals[a] == 'branch']
        branch = branch_arg[0] if branch_arg else None
        repo.herd_remote(self.fork.url(protocol), self.fork.remote_name, branch=branch)

    def _url(self, protocol=None):
        """Return project url

        :param Optional[str] protocol: Git protocol ('ssh' or 'https')
        """

        if protocol:
            return git_url(protocol, self.source.url, self.name)

        return git_url(self._protocol, self.source.url, self.name)
