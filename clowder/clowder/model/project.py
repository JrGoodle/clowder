# -*- coding: utf-8 -*-
"""Representation of clowder.yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import inspect
import os
import sys

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.git.project_repo import ProjectRepo
from clowder.git.project_repo_recursive import ProjectRepoRecursive
from clowder.model.fork import Fork
from clowder.util.connectivity import is_offline
from clowder.util.decorators import project_repo_exists
from clowder.util.execute import execute_forall_command


class Project(object):
    """clowder.yaml Project model class

    :ivar str name: Project name
    :ivar str path: Project relative path
    :ivar Fork fork: Project's associated Fork
    """

    def __init__(self, root_directory, project, group, defaults, sources):
        """Project __init__

        :param str root_directory: Root directory of clowder projects
        :param dict project: Parsed YAML python object for project
        :param dict group: Parsed YAML python object for group
        :param dict defaults: Parsed YAML python object for defaults
        :param list(Source) sources: List of Source instances
        """

        self.name = project['name']
        self.path = project['path']

        self._root_directory = root_directory
        self._ref = project.get('ref', group.get('ref', defaults['ref']))
        self._remote = project.get('remote', group.get('remote', defaults['remote']))
        self._depth = project.get('depth', group.get('depth', defaults['depth']))
        self._recursive = project.get('recursive', group.get('recursive', defaults.get('recursive', False)))
        self._timestamp_author = project.get('timestamp_author', group.get('timestamp_author',
                                                                           defaults.get('timestamp_author', None)))
        self._print_output = True

        self._source = None
        source_name = project.get('source', group.get('source', defaults['source']))
        for source in sources:
            if source.name == source_name:
                self._source = source

        self._url = self._source.get_url_prefix() + self.name + ".git"

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            if fork['remote'] == self._remote:
                error = fmt.remote_name_error(fork['name'], self.name, self._remote)
                print(fmt.invalid_yaml_error())
                print(error + '\n')
                sys.exit(1)
            self.fork = Fork(fork, self._root_directory, self.path, self._source)

    @project_repo_exists
    def branch(self, local=False, remote=False):
        """Print branches for project

        :param Optional[bool] local: Print local branches. Defaults to False
        :param Optional[bool] remote: Print remote branches. Defaults to False
        :return:
        """

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not is_offline():
            if remote:
                if self.fork is None:
                    repo.fetch(self._remote, depth=self._depth)
                else:
                    repo.fetch(self.fork.remote_name)
                    repo.fetch(self._remote)

        repo.print_branches(local=local, remote=remote)

    @project_repo_exists
    def checkout(self, branch):
        """Checkout branch

        :param str branch: Branch to check out
        :return:
        """

        self._repo(self.full_path(), self._remote, self._ref, self._recursive).checkout(branch, allow_failure=True)

    @project_repo_exists
    def clean(self, args='', recursive=False):
        """Discard changes for project

        :param Optional[str] args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param Optional[bool] recursive: Clean submodules recursively. Defaults to False
        :return:
        """

        self._repo(self.full_path(), self._remote, self._ref, self._recursive and recursive).clean(args=args)

    @project_repo_exists
    def clean_all(self):
        """Discard all changes for project

        Equivalent to:
        ``git clean -ffdx; git reset --hard; git rebase --abort``
        ``git submodule foreach --recursive git clean -ffdx``
        ``git submodule foreach --recursive git reset --hard``
        ``git submodule update --checkout --recursive --force``

        :return:
        """

        self._repo(self.full_path(), self._remote, self._ref, self._recursive).clean(args='fdx')

    @project_repo_exists
    def diff(self):
        """Show git diff for project

        Equivalent to: ``git status -vv``

        :return:
        """

        ProjectRepo(self.full_path(), self._remote, self._ref).status_verbose()

    def existing_branch(self, branch, is_remote):
        """Check if branch exists

        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if branch exists
        :rtype: bool
        """

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not is_remote:
            return repo.existing_local_branch(branch)

        remote = self._remote if self.fork is None else self.fork.remote_name
        return repo.existing_remote_branch(branch, remote)

    @project_repo_exists
    def fetch_all(self):
        """Fetch upstream changes if project exists on disk

        :return:
        """

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if self.fork is None:
            repo.fetch(self._remote, depth=self._depth)
            return

        repo.fetch(self.fork.remote_name)
        repo.fetch(self._remote)

    def formatted_project_path(self):
        """Return formatted project path

        :return: Formatted string of full file path
        :rtype: str
        """

        return ProjectRepo.format_project_string(os.path.join(self._root_directory, self.path), self.path)

    def full_path(self):
        """Return full path to project

        :return: Project's full file path
        :rtype: str
        """

        return os.path.join(self._root_directory, self.path)

    def get_current_timestamp(self):
        """Return timestamp of current HEAD commit

        :return: HEAD commit timestamp
        :rtype: str
        """

        return ProjectRepo(self.full_path(), self._remote, self._ref).get_current_timestamp()

    def get_yaml(self, resolved=False):
        """Return python object representation for saving yaml

        :param Optional[bool] resolved: Return default ref rather than current commit sha. Defaults to False
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            ref = self._ref
        else:
            ref = ProjectRepo(self.full_path(), self._remote, self._ref).sha()

        project = {'name': self.name,
                   'path': self.path,
                   'depth': self._depth,
                   'recursive': self._recursive,
                   'ref': ref,
                   'remote': self._remote,
                   'source': self._source.name}

        if self.fork:
            fork_yaml = self.fork.get_yaml()
            project['fork'] = fork_yaml

        if self._timestamp_author:
            project['timestamp_author'] = self._timestamp_author

        return project

    def herd(self, **kwargs):
        """Clone project or update latest from upstream

        Keyword Args:
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
                Defaults to None
            rebase (bool): Whether to use rebase instead of pulling latest changes. Defaults to False
            parallel (bool): Whether command is being run in parallel, affects output. Defaults to False

        :return:
        """

        branch = kwargs.get('branch', None)
        tag = kwargs.get('tag', None)
        depth = kwargs.get('depth', None)
        rebase = kwargs.get('rebase', False)
        parallel = kwargs.get('parallel', False)

        self._print_output = not parallel

        herd_depth = self._depth if depth is None else depth
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive, parallel=parallel)

        if branch:
            fork_remote = None if self.fork is None else self.fork.remote_name
            self._run_herd_command('herd_branch', repo, self._url, branch,
                                   depth=herd_depth, rebase=rebase, fork_remote=fork_remote)
            return

        if tag:
            self._run_herd_command('herd_tag', repo, self._url, tag, depth=herd_depth, rebase=rebase)
            return

        self._run_herd_command('herd', repo, self._url, depth=herd_depth, rebase=rebase)

    def is_dirty(self):
        """Check if project is dirty

        :return: True, if dirty
        :rtype: bool
        """

        return not self._repo(self.full_path(), self._remote, self._ref, self._recursive).validate_repo()

    def is_valid(self):
        """Validate status of project

        :return: True, if not dirty or if the project doesn't exist on disk
        :rtype: bool
        """

        return ProjectRepo(self.full_path(), self._remote, self._ref).validate_repo()

    def print_validation(self):
        """Print validation message for project

        :return:
        """

        if not self.is_valid():
            print(self.status())
            ProjectRepo.print_validation(self.full_path())

    @project_repo_exists
    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branch

        :param str branch: Branch to prune
        :param Optional[bool] force: Force delete branch. Defaults to False
        :param Optional[bool] local: Delete local branch. Defaults to False
        :param Optional[bool] remote: Delete remote branch. Defaults to False
        :return:
        """

        if local and remote:
            self._prune_local(branch, force)
            self._prune_remote(branch)
        elif local:
            self._prune_local(branch, force)
        elif remote:
            self._prune_remote(branch)

    def reset(self, timestamp=None, parallel=False):
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        :return:
        """

        self._print_output = not parallel

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive, parallel=parallel)
        self._reset(repo, timestamp=timestamp)

    def run(self, command, ignore_errors, parallel=False):
        """Run command or script in project directory

        :param str command: Command to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        :return:
        """

        if not parallel:
            if not ProjectRepo.existing_git_repository(self.full_path()):
                print(colored(" - Project is missing\n", 'red'))
                return

        self._print_output = not parallel
        self._print(fmt.command(command))

        forall_env = {'CLOWDER_PATH': self._root_directory,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self._remote,
                      'PROJECT_REF': self._ref}

        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote_name

        return_code = execute_forall_command(command.split(), self.full_path(), forall_env, self._print_output)
        if not ignore_errors:
            err = fmt.command_failed_error(command)
            if return_code != 0:
                self._print(err)
                self._exit(err, return_code=return_code, parallel=parallel)

    @project_repo_exists
    def start(self, branch, tracking):
        """Start a new feature branch

        :param str branch: Local branch name to create
        :param bool tracking: Whether to create a remote branch with tracking relationship
        :return:
        """

        remote = self._remote if self.fork is None else self.fork.remote_name
        depth = self._depth if self.fork is None else 0
        ProjectRepo(self.full_path(), self._remote, self._ref).start(remote, branch, depth, tracking)

    def status(self, padding=None):
        """Return formatted status for project

        :param Optional[int] padding: Amount of padding to use for printing project on left and current ref on right
        :return: Formatting project name and status
        :rtype: str
        """

        if not ProjectRepo.existing_git_repository(self.full_path()):
            return colored(self.name, 'green')

        project_output = ProjectRepo.format_project_string(self.full_path(), self.path)
        current_ref_output = ProjectRepo.format_project_ref_string(self.full_path())

        if padding:
            project_output = project_output.ljust(padding)

        return project_output + ' ' + current_ref_output

    @project_repo_exists
    def stash(self):
        """Stash changes for project if dirty

        :return:
        """

        if self.is_dirty():
            ProjectRepo(self.full_path(), self._remote, self._ref).stash()

    def sync(self, rebase=False, parallel=False):
        """Sync fork project with upstream remote

        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        :return:
        """

        self._print_output = not parallel

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive, parallel=parallel)
        self._run_herd_command('herd', repo, self._url, rebase=rebase)
        self._print(self.fork.status())
        repo.sync(self.fork.remote_name, rebase=rebase)

    @staticmethod
    def _exit(message, parallel=False, return_code=1):
        """Exit based on serial or parallel job

        :param str message: Branch to check for
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output. Defaults to False
        :param Optional[int] return_code: Return code for sys.exit()
        :return:
        :raise ClowderError: General ClowderError with message
        """

        if parallel:
            raise ClowderError(message)
        sys.exit(return_code)

    def _print(self, val):
        """Print output if self._print_output is True

        :param str val: String to print
        :return:
        """

        if self._print_output:
            print(val)

    def _prune_local(self, branch, force):
        """Prune local branch

        :param str branch: Local branch to delete
        :param bool force: Force delete branch
        :return:
        """

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if repo.existing_local_branch(branch):
            repo.prune_branch_local(branch, force)

    def _prune_remote(self, branch):
        """Prune remote branch

        :param str branch: Remote branch to delet
        :return:
        """

        remote = self._remote if self.fork is None else self.fork.remote_name
        repo = ProjectRepo(self.full_path(), remote, self._ref)
        if repo.existing_remote_branch(branch, remote):
            repo.prune_branch_remote(branch, remote)

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

        :return:
        """

        if recursive:
            return ProjectRepoRecursive(path, remote, ref, **kwargs)
        return ProjectRepo(path, remote, ref, **kwargs)

    def _reset(self, repo, timestamp=None):
        """Reset project branch to upstream or checkout tag/sha as detached HEAD

        :param ProjectRepo repo: ProjectRepo or ProjectRepoRecursive instance
        :param Optional[str] timestamp: Reset to commit at timestamp, or closest previous commit
        :return:
        """

        if self.fork is None:
            if timestamp:
                repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
                return

            repo.reset(depth=self._depth)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)

        self._print(fmt.fork_string(self.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
            return

        repo.reset()

    def _run_herd_command(self, command, repo, *args, **kwargs):
        """Run herd command

        :param str command: Repo path
        :param ProjectRepo repo: ProjectRepo or ProjectRepoRecursive instance
        :param str ref: Default repo ref

        Other Parameters:
            url (str): URL to clone from
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd

        Keyword Args:
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
            rebase (bool): Whether to use rebase instead of pulling latest changes
            fork_remote (str): Fork remote name

        :return:
        """

        if self.fork is None:
            getattr(repo, command)(*args, **kwargs)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)

        self._print(fmt.fork_string(self.name))
        kwargs['depth'] = 0
        getattr(repo, command)(*args, **kwargs)

        self._print(fmt.fork_string(self.fork.name))

        frame = inspect.currentframe()
        vals = inspect.getargvalues(frame)
        branch_arg = [a for a in vals.args if vals.locals[a] if vals.locals[a] == 'branch']
        branch = branch_arg[0] if branch_arg else None
        repo.herd_remote(self.fork.url, self.fork.remote_name, branch=branch)
