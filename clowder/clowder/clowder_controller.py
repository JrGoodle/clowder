# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import multiprocessing as mp
import os
import signal
import sys

import psutil

import clowder.util.formatting as fmt
import clowder.yaml.printing as yaml_print
import clowder.yaml.saving as yaml_save
from clowder.error.clowder_error import ClowderError
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.util.progress import Progress
from clowder.yaml.loading import load_yaml
from clowder.yaml.validating import validate_yaml
from termcolor import cprint


def herd_project(project, branch, tag, depth, rebase):
    """Herd command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str branch: Branch to attempt to herd
    :param str tag: Tag to attempt to herd
    :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, parallel=True)


def reset_project(project, timestamp):
    """Reset command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str timestamp: If not None, reset to commit at timestamp, or closest previous commit
    """

    project.reset(timestamp=timestamp, parallel=True)


def run_project(project, command, ignore_errors):
    """Run command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str command: Command to run
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    """

    project.run(command, ignore_errors, parallel=True)


def sync_project(project, rebase):
    """Sync command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    project.sync(rebase, parallel=True)


def async_callback(val):
    """Increment async progress bar

    :param val: Dummy parameter to satisfy callback interface
    """

    del val
    __clowder_progress__.update()


__clowder_parent_id__ = os.getpid()


def worker_init():
    """
    Process pool terminator

    .. note:: Implementation source https://stackoverflow.com/a/45259908
    """

    def sig_int(signal_num, frame):
        """Signal handler

        :param signal_num: Dummy parameter to satisfy callback interface
        :param frame: Dummy parameter to satisfy callback interface
        """

        del signal_num, frame
        parent = psutil.Process(__clowder_parent_id__)
        for child in parent.children(recursive=True):
            if child.pid != os.getpid():
                child.terminate()
        parent.terminate()
        psutil.Process(os.getpid()).terminate()
        print('\n\n')

    signal.signal(signal.SIGINT, sig_int)


__clowder_results__ = []
__clowder_pool__ = mp.Pool(initializer=worker_init)
__clowder_progress__ = Progress()


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar str root_directory: Root directory of clowder projects
    :ivar dict defaults: Global clowder.yaml defaults
    :ivar list(Group) groups: List of all Groups
    :ivar list(Source) sources: List of all Sources
    """

    def __init__(self, root_directory):
        """ClowderController __init__

        :param str root_directory: Root directory of clowder projects
        """

        self.root_directory = root_directory
        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10
        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')

        try:
            validate_yaml(yaml_file, self.root_directory)
        except ClowderError:
            raise
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        else:
            self._load_yaml()

    def branch(self, group_names, **kwargs):
        """Print branches

        .. py:function:: branch(group_names, local=False, remote=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to print branches for
        :param bool local: Print local branches
        :param bool remote: Print remote branches
        :param list(str) project_names: Project names to print branches for
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        local = kwargs.get('local', False)
        remote = kwargs.get('remote', False)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'branch', local=local, remote=remote)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'branch', local=local, remote=remote)

    def checkout(self, branch, group_names, **kwargs):
        """Checkout branches

        .. py:function:: checkout(branch, group_names, project_names=None, skip=[])

        :param str branch: Branch to checkout
        :param list(str) group_names: Group names to checkout branches for
        :param list(str) project_names: Project names to clean
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'checkout', branch)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'checkout', branch)

    def clean(self, group_names, **kwargs):
        """Discard changes

        .. py:function:: clean(group_names, args='', recursive=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to clean
        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :param bool recursive: Clean submodules recursively
        :param list(str) project_names: Project names to clean
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        args = kwargs.get('args', '')
        recursive = kwargs.get('recursive', False)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'clean', args=args, recursive=recursive)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'clean', args=args, recursive=recursive)

    def clean_all(self, group_names, **kwargs):
        """Discard all changes

        .. py:function:: clean_all(group_names, project_names=None, skip=[])

        :param list(str) group_names: Group names to clean
        :param list(str) project_names: Project names to clean
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'clean_all')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'clean_all')

    def diff(self, group_names, project_names=None):
        """Show git diff

        :param list(str) group_names: Group names to print diffs for
        :param Optional[list(str)] project_names: Project names to print diffs for. Defaults to None
        """

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, [], 'diff')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            print(project.status())
            project.diff()

    def fetch(self, group_names):
        """Fetch groups

        :param list(str) group_names: Group names to fetch
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            self._run_group_command(group, [], 'fetch_all')

    def forall(self, command, ignore_errors, group_names, **kwargs):
        """Runs command or script in project directories specified

        .. py:function:: forall(command, ignore_errors, group_names, project_names=None, skip=[], parallel=False)

        :param str command: Command to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param list(str) group_names: Group names to run command for
        :param list(str) project_names: Project names to clean
        :param list(str) skip: Project names to skip
        :param bool parallel: Whether command is being run in parallel, affects output
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        parallel = kwargs.get('parallel', False)

        if project_names is None:
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]

        if parallel:
            self._forall_parallel(command, skip, ignore_errors, projects)
            return

        for project in projects:
            self._run_project_command(project, skip, 'run', command, ignore_errors)

    def get_all_fork_project_names(self):
        """Returns all project names containing forks

        :return: List of project names containing forks
        :rtype: list(str)
        """

        return sorted([p.name for g in self.groups for p in g.projects if p.fork])

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml

        :return: List of all group names
        :rtype: list(str)
        """

        return sorted([g.name for g in self.groups])

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list(str)
        """

        return sorted([p.name for g in self.groups for p in g.projects])

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list(str)
        """

        return sorted([p.formatted_project_path() for g in self.groups for p in g.projects])

    def get_saved_version_names(self):
        """Return list of all saved versions

        :return: List of all saved version names
        :rtype: list(str)
        """

        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        if not os.path.exists(versions_dir):
            return None
        return [v for v in os.listdir(versions_dir) if not v.startswith('.') if v.lower() != 'default']

    def herd(self, group_names, **kwargs):
        """Clone projects or update latest from upstream

        .. py:function:: herd(group_names, branch=None, tag=None, depth=0, rebase=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to herd
        :param str branch: Branch to attempt to herd
        :param str tag: Tag to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        :param list(str) project_names: Project names to herd
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        branch = kwargs.get('branch', None)
        tag = kwargs.get('tag', None)
        depth = kwargs.get('depth', None)
        rebase = kwargs.get('rebase', False)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            for group in groups:
                self._run_group_command(group, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)

    def herd_parallel(self, group_names, **kwargs):
        """Clone projects or update latest from upstream in parallel

        .. py:function:: herd_parallel(group_names, branch=None, tag=None, depth=0, rebase=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to herd
        :param str branch: Branch to attempt to herd
        :param str tag: Tag to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        :param list(str) project_names: Project names to herd
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        branch = kwargs.get('branch', None)
        tag = kwargs.get('tag', None)
        depth = kwargs.get('depth', None)
        rebase = kwargs.get('rebase', False)

        print(' - Herd projects in parallel\n')
        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
            self._print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                      callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    def print_yaml(self, resolved):
        """Print clowder.yaml

        :param bool resolved: Print default ref rather than current commit sha
        """

        if resolved:
            print(fmt.yaml_string(self._get_yaml_resolved()))
        else:
            yaml_print.print_yaml(self.root_directory)
        sys.exit()  # exit early to prevent printing extra newline

    def prune(self, group_names, branch, **kwargs):
        """Prune branches

        .. py:function:: prune(group_names, local=False, remote=False, force=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to prune branches for
        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        :param list(str) project_names: Project names to prune
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        force = kwargs.get('force', False)
        local = kwargs.get('local', False)
        remote = kwargs.get('remote', False)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            self._prune_groups(groups, branch, skip=skip, force=force, local=local, remote=remote)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._prune_projects(projects, branch, skip=skip, force=force, local=local, remote=remote)

    def reset(self, group_names, **kwargs):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD

        .. py:function:: reset(group_names, timestamp_project=None, parallel=False, project_names=None, skip=[])

        :param list(str) group_names: Group names to reset
        :param str timestamp_project: Reference project to checkout commit timestamps of other projects relative to
        :param bool parallel: Whether command is being run in parallel, affects output
        :param list(str) project_names: Project names to reset
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        timestamp_project = kwargs.get('timestamp_project', None)
        parallel = kwargs.get('parallel', False)

        if parallel:
            self._reset_parallel(group_names, skip=skip, timestamp_project=timestamp_project)
            return

        timestamp = None
        if timestamp_project:
            timestamp = self._get_timestamp(timestamp_project)
        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            for group in groups:
                self._run_group_command(group, skip, 'reset', timestamp=timestamp)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'reset', timestamp=timestamp)

    def save_version(self, version):
        """Save current commits to a clowder.yaml in the versions directory

        :param str version: Name of saved version
        """

        self._validate_projects_exist()
        self._validate_groups(self.groups)
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        version_name = version.replace('/', '-')  # Replace path separators with dashes
        version_dir = os.path.join(versions_dir, version_name)
        if not os.path.exists(version_dir):
            try:
                os.makedirs(version_dir)
            except OSError as err:
                if err.errno != os.errno.EEXIST:
                    raise

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        if os.path.exists(yaml_file):
            print(fmt.save_version_exists_error(version_name, yaml_file) + '\n')
            sys.exit(1)

        print(fmt.save_version(version_name, yaml_file))
        yaml_save.save_yaml(self._get_yaml(), yaml_file)

    def start_groups(self, group_names, skip, branch, tracking=False):
        """Start feature branch for groups

        :param list(str) group_names: Group names to create branches for
        :param list(str) skip: Project names to skip
        :param str branch: Local branch name to create
        :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
            Defaults to False
        """

        groups = [g for g in self.groups if g.name in group_names]
        self._validate_groups(groups)
        for group in groups:
            self._run_group_command(group, skip, 'start', branch, tracking)

    def start_projects(self, project_names, skip, branch, tracking=False):
        """Start feature branch for projects

        :param list(str) project_names: Project names to creat branches for
        :param list(str) skip: Project names to skip
        :param str branch: Local branch name to create
        :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
            Defaults to False
        """

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'start', branch, tracking)

    def stash(self, group_names, **kwargs):
        """Stash changes for projects with changes

        .. py:function:: clean(group_names, project_names=None, skip=[])

        :param list(str) group_names: Group names to stash
        :param list(str) project_names: Project names to clean
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])

        if not self._is_dirty():
            print('No changes to stash')
            return

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'stash')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'stash')

    def status(self, group_names, padding):
        """Print status for groups

        :param list(str) group_names: Group names to print status for
        :param int padding: Amount of padding to use for printing project on left and current ref on right
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                print(project.status(padding=padding))

    def sync(self, project_names, rebase=False, parallel=False):
        """Sync projects

        :param list(str) project_names: Project names to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes.
            Defaults to False
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output.
            Defaults to False
        """

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        if parallel:
            self._sync_parallel(projects, rebase=rebase)
            return

        for project in projects:
            project.sync(rebase=rebase)

    @staticmethod
    def _existing_branch_groups(groups, branch, is_remote):
        """Checks if given branch exists in any project

        :param list(Group) groups: Groups to check
        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        :rtype: bool
        """

        return any([p.existing_branch(branch, is_remote=is_remote) for g in groups for p in g.projects])

    @staticmethod
    def _existing_branch_projects(projects, branch, is_remote):
        """Checks if given branch exists in any project

        :param list(Project) projects: Projects to check
        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        :rtype: bool
        """

        return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])

    def _fetch_groups(self, group_names):
        """Fetch all projects for specified groups

        :param list(str) group_names: Group names to fetch
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.fetch_all()

    def _fetch_projects(self, project_names):
        """Fetch specified projects

        :param list(str) project_names: Project names to fetch
        """

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            project.fetch_all()

    @staticmethod
    def _forall_parallel(command, skip, ignore_errors, projects):
        """Runs command or script for projects in parallel

        :param str command: Command to run
        :param list(str) skip: Project names to skip
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param list(Project) projects: Projects to run command for
        """

        print(' - Run forall commands in parallel\n')
        for project in projects:
            if project.name in skip:
                continue
            print(project.status())
            if not os.path.isdir(project.full_path()):
                cprint(" - Project is missing", 'red')

        print('\n' + fmt.command(command))
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(run_project, args=(project, command, ignore_errors),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def _get_timestamp(self, timestamp_project):
        """Return timestamp for project

        :param str timestamp_project: Project to get timestamp of current HEAD commit
        :return: Commit timestamp string
        :rtype: str
        """

        timestamp = None
        all_projects = [p for g in self.groups for p in g.projects]
        for project in all_projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            cprint(' - Failed to find timestamp\n', 'red')
            sys.exit(1)

        return timestamp

    def _get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def _get_yaml_resolved(self):
        """Return python object representation for resolved yaml

        :return: YAML python object
        :rtype: dict
        """

        groups_yaml = [g.get_yaml_resolved() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def _is_dirty(self):
        """Check if there are any dirty projects

        :return: True, if dirty
        :rtype: bool
        """

        return any([g.is_dirty() for g in self.groups])

    def _load_yaml(self):
        """Load clowder.yaml"""
        yaml = load_yaml(self.root_directory)

        self.defaults = yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in yaml['sources']]
        for group in yaml['groups']:
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))

    @staticmethod
    def _print_parallel_groups_output(groups, skip):
        """Print output for parallel group command

        :param list(Group) groups: Groups to print output for
        :param list(str) skip: Project names to skip
        """

        for group in groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                if project.name in skip:
                    continue
                print(project.status())
                if project.fork:
                    print('  ' + fmt.fork_string(project.name))
                    print('  ' + fmt.fork_string(project.fork.name))

    @staticmethod
    def _print_parallel_projects_output(projects, skip):
        """Print output for parallel project command

        :param list(Project) projects: Projects to print output for
        :param list(str) skip: Project names to skip
        """

        for project in projects:
            if project.name in skip:
                continue
            print(project.status())
            if project.fork:
                print('  ' + fmt.fork_string(project.name))
                print('  ' + fmt.fork_string(project.fork.name))

    def _prune_groups(self, groups, branch, **kwargs):
        """Prune group branches

        .. py:function:: _prune_groups(groups, branch, local=False, remote=False, force=False, skip=[])

        :param list(Group) groups: Groups to prune
        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        :param list(str) skip: Project names to skip
        """

        skip = kwargs.get('skip', [])
        force = kwargs.get('force', False)
        local = kwargs.get('local', False)
        remote = kwargs.get('remote', False)

        if local and remote:
            local_branch_exists = self._existing_branch_groups(groups, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_groups(groups, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()

            print(' - Prune local and remote branches\n')
            for group in groups:
                local_branch_exists = group.existing_branch(branch, is_remote=False)
                remote_branch_exists = group.existing_branch(branch, is_remote=True)
                if local_branch_exists or remote_branch_exists:
                    self._run_group_command(group, skip, 'prune', branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_groups(groups, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()

            for group in groups:
                if group.existing_branch(branch, is_remote=False):
                    self._run_group_command(group, skip, 'prune', branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_groups(groups, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()

            for group in groups:
                if group.existing_branch(branch, is_remote=True):
                    self._run_group_command(group, skip, 'prune', branch, remote=True)

    def _prune_projects(self, projects, branch, **kwargs):
        """Prune project branches

        .. py:function:: _prune_projects(projects, branch, local=False, remote=False, force=False, skip=[])

        :param list(Project) projects: Projects to prune
        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        :param list(str) skip: Project names to skip
        """

        skip = kwargs.get('skip', [])
        force = kwargs.get('force', False)
        local = kwargs.get('local', False)
        remote = kwargs.get('remote', False)

        if local and remote:
            local_branch_exists = self._existing_branch_projects(projects, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_projects(projects, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()

            print(' - Prune local and remote branches\n')
            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_projects(projects, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()

            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_projects(projects, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()

            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, remote=True)

    def _reset_parallel(self, group_names, **kwargs):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

        .. py:function:: _reset_parallel(group_names, timestamp_project=None, project_names=None, skip=[])

        :param list(str) group_names: Group names to reset
        :param str timestamp_project: Reference project to checkout commit timestamps of other projects relative to
        :param list(str) project_names: Project names to reset
        :param list(str) skip: Project names to skip
        """

        project_names = kwargs.get('project_names', None)
        skip = kwargs.get('skip', [])
        timestamp_project = kwargs.get('timestamp_project', None)

        print(' - Reset projects in parallel\n')
        timestamp = None
        if timestamp_project:
            timestamp = self._get_timestamp(timestamp_project)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
            self._print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    @staticmethod
    def _run_group_command(group, skip, command, *args, **kwargs):
        """Run group command and print output

        :param Group group: Group to run command for
        :param list(str) skip: Project names to skip
        :param str command: Name of method to invoke
        :param args: List of arguments to pass to method invocation
        :param kwargs: Dict of arguments to pass to method invocation
        """

        print(fmt.group_name(group.name))
        for project in group.projects:
            print(project.status())
            if project.name in skip:
                print(fmt.skip_project_message())
                continue
            getattr(project, command)(*args, **kwargs)

    @staticmethod
    def _run_project_command(project, skip, command, *args, **kwargs):
        """Run project command and print output

        :param Praject project: Project to run command for
        :param list(str) skip: Project names to skip
        :param str command: Name of method to invoke
        :param args: List of arguments to pass to method invocation
        :param kwargs: Dict of arguments to pass to method invocation
        """

        print(project.status())
        if project.name in skip:
            print(fmt.skip_project_message())
            return
        getattr(project, command)(*args, **kwargs)

    @staticmethod
    def _sync_parallel(projects, rebase=False):
        """Sync projects in parallel

        :param list(Project) projects: Projects to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        """

        print(' - Sync forks in parallel\n')
        for project in projects:
            print(project.status())
            if project.fork:
                print('  ' + fmt.fork_string(project.name))
                print('  ' + fmt.fork_string(project.fork.name))

        for project in projects:
            result = __clowder_pool__.apply_async(sync_project, args=(project, rebase), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    @staticmethod
    def _validate_groups(groups):
        """Validate status of all projects for specified groups

        :param list(Group) groups: Groups to validate
        """

        for group in groups:
            group.print_validation()

        if not all([g.is_valid() for g in groups]):
            print()
            sys.exit(1)

    @staticmethod
    def _validate_projects(projects):
        """Validate status of all projects

        :param list(Project) projects: Projects to validate
        """

        if not all([p.is_valid() for p in projects]):
            print()
            sys.exit(1)

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups"""

        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.existing_projects():
                projects_exist = False

        if not projects_exist:
            herd_output = fmt.clowder_command('clowder herd')
            print('\n - First run ' + herd_output + ' to clone missing projects\n')
            sys.exit(1)


# Disable warnings shown by pylint for catching too general exception
# pylint: disable=W0703


def pool_handler(count):
    """Pool handler for finishing parallel jobs

    :param int count: Total count of projects in progress bar
    """

    print()
    __clowder_progress__.start(count)

    try:
        for result in __clowder_results__:
            result.get()
            if not result.successful():
                __clowder_progress__.close()
                __clowder_pool__.close()
                __clowder_pool__.terminate()
                cprint('\n - Command failed\n', 'red')
                sys.exit(1)
    except Exception as err:
        __clowder_progress__.close()
        __clowder_pool__.close()
        __clowder_pool__.terminate()
        cprint('\n' + str(err) + '\n', 'red')
        sys.exit(1)
    else:
        __clowder_progress__.complete()
        __clowder_progress__.close()
        __clowder_pool__.close()
        __clowder_pool__.join()
