# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import multiprocessing as mp
import os
import signal
import sys

import clowder.util.formatting as fmt
import clowder.yaml.loading as yaml_load
import clowder.yaml.parsing as yaml_parse
import clowder.yaml.printing as yaml_print
import clowder.yaml.saving as yaml_save
import clowder.yaml.validation.validation as yaml_validate
import psutil
from clowder.error.clowder_error import ClowderError
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.util.progress import Progress
from termcolor import cprint


def herd_project(project, branch, tag, depth, rebase):
    """Herd command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str branch: Branch to attempt to herd
    :param str tag: Tag to attempt to herd
    :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    :return:
    """

    project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, parallel=True)


def reset_project(project, timestamp):
    """Reset command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str timestamp: If not None, reset to commit at timestamp, or closest previous commit
    :return:
    """

    project.reset(timestamp=timestamp, parallel=True)


def run_project(project, command, ignore_errors):
    """Run command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str command: Command to run
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :return:
    """

    project.run(command, ignore_errors, parallel=True)


def sync_project(project, rebase):
    """Sync command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    :return:
    """

    project.sync(rebase, parallel=True)


def async_callback(val):
    """Increment async progress bar

    :param val: Dummy parameter to satisfy callback interface
    :return:
    """

    del val
    __clowder_progress__.update()


__clowder_parent_id__ = os.getpid()


def worker_init():
    """
    Process pool terminator

    .. note:: Implementation source https://stackoverflow.com/a/45259908

    :return:
    """

    def sig_int(signal_num, frame):
        """Signal handler

        :param signal_num: Dummy parameter to satisfy callback interface
        :param frame: Dummy parameter to satisfy callback interface
        :return:
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

    Attributes:
        root_directory (str): Root directory of clowder projects
        defaults (dict): Global clowder.yaml defaults
        groups (list of Group): List of all Groups
        sources (list of Source): List of all Sources
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
            self._validate_yaml(yaml_file, self._max_import_depth)
        except ClowderError:
            raise
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        else:
            self._load_yaml()

    def branch(self, group_names, **kwargs):
        """Print branches

        :param list of str group_names: Group names to print branches for

        Keyword Args:
            local (bool): Print local branches. Defaults to False
            remote (bool): Print remote branches. Defaults to False
            project_names (list of str): Project names to print branches for
            skip (list of str): Project names to skip

        :return:
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

    def clean(self, group_names, **kwargs):
        """Discard changes

        :param list of str group_names: Group names to clean

        Keyword Args:
            args (str): Git clean options
                - ``d`` Remove untracked directories in addition to untracked files
                - ``f`` Delete directories with .git sub directory or file
                - ``X`` Remove only files ignored by git
                - ``x`` Remove all untracked files
            recursive (bool): Clean submodules recursively. Defaults to False
            project_names (list of str): Project names to clean
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to clean

        Keyword Args:
            project_names (list of str): Project names to clean
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to print diffs for
        :param Optional[list of str] project_names: Project names to print diffs for. Defaults to None
        :return:
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

        :param list of str group_names: Group names to fetch
        :return:
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            self._run_group_command(group, [], 'fetch_all')

    def forall(self, command, ignore_errors, group_names, **kwargs):
        """Runs command or script in project directories specified

        :param str command: Command to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param list of str group_names: Group names to run command for

        Keyword Args:
            project_names (list of str): Project names to run command for
            skip (list of str): Project names to skip
            parallel (bool): Whether command is being run in parallel, affects output. Defaults to False

        :return:
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
        :rtype: list of str
        """

        return sorted([p.name for g in self.groups for p in g.projects if p.fork])

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml

        :return: List of all group names
        :rtype: list of str
        """

        return sorted([g.name for g in self.groups])

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list of str
        """

        return sorted([p.name for g in self.groups for p in g.projects])

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list of str
        """

        return sorted([p.formatted_project_path() for g in self.groups for p in g.projects])

    def get_saved_version_names(self):
        """Return list of all saved versions

        :return: List of all saved version names
        :rtype: list of str
        """

        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        if not os.path.exists(versions_dir):
            return None
        return [v for v in os.listdir(versions_dir) if not v.startswith('.') if v.lower() != 'default']

    def herd(self, group_names, **kwargs):
        """Clone projects or update latest from upstream

        :param list of str group_names: Group names to herd

        Keyword Args:
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
                Defaults to None
            rebase (bool): Whether to use rebase instead of pulling latest changes. Defaults to False
            project_names (list of str): Project names to herd
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to herd

        Keyword Args:
            branch (str): Branch to attempt to herd
            tag (str): Tag to attempt to herd
            depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
                Defaults to None
            rebase (bool): Whether to use rebase instead of pulling latest changes. Defaults to False
            project_names (list of str): Project names to herd
            skip (list of str): Project names to skip

        :return:
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
        :return:
        """

        if resolved:
            print(fmt.yaml_string(self._get_yaml_resolved()))
        else:
            yaml_print.print_yaml(self.root_directory)
        sys.exit()  # exit early to prevent printing extra newline

    def prune(self, group_names, branch, **kwargs):
        """Prune branches

        :param list of str group_names: Group names to prune branches for
        :param str branch: Branch to prune

        Keyword Args:
            force (bool): Force delete branch. Defaults to False
            local (bool): Delete local branch. Defaults to False
            remote (bool): Delete remote branch. Defaults to False
            project_names (list of str): Project names to prune
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to reset

        Keyword Args:
            timestamp_project (str): Reference project to checkout commit timestamps of other projects relative to
            parallel (bool): Whether command is being run in parallel, affects output. Defaults to False
            project_names (list of str): Project names to reset
            skip (list of str): Project names to skip

        :return:
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
        :return:
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

        :param list of str group_names: Group names to create branches for
        :param list of str skip: Project names to skip
        :param str branch: Local branch name to create
        :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
            Defaults to False
        :return:
        """

        groups = [g for g in self.groups if g.name in group_names]
        self._validate_groups(groups)
        for group in groups:
            self._run_group_command(group, skip, 'start', branch, tracking)

    def start_projects(self, project_names, skip, branch, tracking=False):
        """Start feature branch for projects

        :param list of str project_names: Project names to creat branches for
        :param list of str skip: Project names to skip
        :param str branch: Local branch name to create
        :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
            Defaults to False
        :return:
        """

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'start', branch, tracking)

    def stash(self, group_names, **kwargs):
        """Stash changes for projects with changes

        :param list of str group_names: Group names to stash

        Keyword Args:
            project_names (list of str): Project names to stash
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to print status for
        :param int padding: Amount of padding to use for printing project on left and current ref on right
        :return:
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                print(project.status(padding=padding))

    def sync(self, project_names, rebase=False, parallel=False):
        """Sync projects

        :param list of str project_names: Project names to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes.
            Defaults to False
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output.
            Defaults to False
        :return:
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

        :param list of Group groups: Groups to check
        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        :rtype: bool
        """

        return any([p.existing_branch(branch, is_remote=is_remote) for g in groups for p in g.projects])

    @staticmethod
    def _existing_branch_projects(projects, branch, is_remote):
        """Checks if given branch exists in any project

        :param list of Project projects: Projects to check
        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        :rtype: bool
        """

        return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])

    def _fetch_groups(self, group_names):
        """Fetch all projects for specified groups

        :param list of str group_names: Group names to fetch
        :return:
        """

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.fetch_all()

    def _fetch_projects(self, project_names):
        """Fetch specified projects

        :param list of str project_names: Project names to fetch
        :return:
        """

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            project.fetch_all()

    @staticmethod
    def _forall_parallel(command, skip, ignore_errors, projects):
        """Runs command or script for projects in parallel

        :param str command: Command to run
        :param list of str skip: Project names to skip
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param list of Project projects: Projects to run command for
        :return:
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
        """Load clowder from yaml file

        :return:
        """

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        parsed_yaml = yaml_parse.parse_yaml(yaml_file)
        imported_yaml_files = []
        combined_yaml = {}
        while True:
            if 'import' not in parsed_yaml:
                yaml_load.load_yaml_base(parsed_yaml, combined_yaml)
                break
            imported_yaml_files.append(parsed_yaml)
            imported_yaml = parsed_yaml['import']

            if imported_yaml == 'default':
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_yaml, 'clowder.yaml')

            parsed_yaml = yaml_parse.parse_yaml(imported_yaml_file)
            if len(imported_yaml_files) > self._max_import_depth:
                print(fmt.invalid_yaml_error())
                print(fmt.recursive_import_error(self._max_import_depth) + '\n')
                sys.exit(1)

        for parsed_yaml in reversed(imported_yaml_files):
            yaml_load.load_yaml_import(parsed_yaml, combined_yaml)

        self._load_yaml_combined(combined_yaml)

    def _load_yaml_combined(self, combined_yaml):
        """Load clowder from combined yaml

        :param dict combined_yaml: Combined yaml
        :return:
        """

        self.defaults = combined_yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in combined_yaml['sources']]
        for group in combined_yaml['groups']:
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))

    @staticmethod
    def _print_parallel_groups_output(groups, skip):
        """Print output for parallel group command

        :param list of Group groups: Groups to print output for
        :param list of str skip: Project names to skip
        :return:
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

        :param list of Project projects: Projects to print output for
        :param list of str skip: Project names to skip
        :return:
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

        :param list of Group groups: Groups to prune
        :param str branch: Branch to prune

        Keyword Args:
            force (bool): Force delete branch. Defaults to False
            local (bool): Delete local branch. Defaults to False
            remote (bool): Delete remote branch. Defaults to False
            skip (list of str): Project names to skip

        :return:
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

        :param list of Project projects: Projects to prune
        :param str branch: Branch to prune

        Keyword Args:
            force (bool): Force delete branch. Defaults to False
            local (bool): Delete local branch. Defaults to False
            remote (bool): Delete remote branch. Defaults to False
            skip (list of str): Project names to skip

        :return:
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

        :param list of str group_names: Group names to reset

        Keyword Args:
            timestamp_project (str): Reference project to checkout commit timestamps of other projects relative to
            project_names (list of str): Project names to herd
            skip (list of str): Project names to skip

        :return:
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
        :param list of str skip: Project names to skip
        :param str command: Name of method to invoke
        :param args: List of arguments to pass to method invocation
        :param kwargs: Dict of arguments to pass to method invocation
        :return:
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
        :param list of str skip: Project names to skip
        :param str command: Name of method to invoke
        :param args: List of arguments to pass to method invocation
        :param kwargs: Dict of arguments to pass to method invocation
        :return:
        """

        print(project.status())
        if project.name in skip:
            print(fmt.skip_project_message())
            return
        getattr(project, command)(*args, **kwargs)

    @staticmethod
    def _sync_parallel(projects, rebase=False):
        """Sync projects in parallel

        :param list of Project projects: Projects to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        :return:
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

        :param list of Group groups: Groups to validate
        :return:
        """

        for group in groups:
            group.print_validation()

        if not all([g.is_valid() for g in groups]):
            print()
            sys.exit(1)

    @staticmethod
    def _validate_projects(projects):
        """Validate status of all projects

        :param list of Project projects: Projects to validate
        :return:
        """

        if not all([p.is_valid() for p in projects]):
            print()
            sys.exit(1)

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups

        :return:
        """

        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.existing_projects():
                projects_exist = False

        if not projects_exist:
            herd_output = fmt.clowder_command('clowder herd')
            print('\n - First run ' + herd_output + ' to clone missing projects\n')
            sys.exit(1)

    def _validate_yaml(self, yaml_file, max_import_depth):
        """Validate clowder.yaml

        :param str yaml_file: Yaml file path to validate
        :param int max_import_depth: Max depth of clowder.yaml imports
        :return:
        """

        parsed_yaml = yaml_parse.parse_yaml(yaml_file)
        if max_import_depth < 0:
            print(fmt.invalid_yaml_error())
            print(fmt.recursive_import_error(self._max_import_depth) + '\n')
            sys.exit(1)

        if 'import' not in parsed_yaml:
            yaml_validate.validate_yaml(yaml_file)
            return

        yaml_validate.validate_yaml_import(yaml_file)
        imported_clowder = parsed_yaml['import']

        try:
            if imported_clowder == 'default':
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_clowder, 'clowder.yaml')
            if not os.path.isfile(imported_yaml_file):
                error = fmt.missing_imported_yaml_error(imported_yaml_file, yaml_file)
                raise ClowderError(error)
            yaml_file = imported_yaml_file
            self._validate_yaml(yaml_file, max_import_depth - 1)
        except ClowderError as err:
            print(fmt.invalid_yaml_error())
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)


# Disable warnings shown by pylint for catching too general exception
# pylint: disable=W0703


def pool_handler(count):
    """Pool handler for finishing parallel jobs

    :param int count: Total count of projects in progress bar
    :return:
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
