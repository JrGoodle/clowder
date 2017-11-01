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
from clowder.commands.util import (
    filter_groups,
    filter_projects_on_group_names,
    filter_projects_on_project_names,
    print_parallel_groups_output,
    print_parallel_projects_output,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)
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
            projects = filter_projects_on_group_names(self.groups, group_names)
        else:
            projects = filter_projects_on_project_names(self.groups, project_names)

        if parallel:
            self._forall_parallel(command, skip, ignore_errors, projects)
            return

        for project in projects:
            run_project_command(project, skip, 'run', command, ignore_errors)

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

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def get_yaml_resolved(self):
        """Return python object representation for resolved yaml

        :return: YAML python object
        :rtype: dict
        """

        groups_yaml = [g.get_yaml_resolved() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

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
            groups = filter_groups(self.groups, group_names)
            validate_groups(groups)
            for group in groups:
                run_group_command(group, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
            return

        projects = filter_projects_on_project_names(self.groups, project_names)
        validate_projects(projects)
        for project in projects:
            run_project_command(project, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)

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
            groups = filter_groups(self.groups, group_names)
            validate_groups(groups)
            projects = filter_projects_on_group_names(self.groups, group_names)
            print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                      callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = filter_projects_on_project_names(self.groups, project_names)
        validate_projects(projects)
        print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

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
            groups = filter_groups(self.groups, group_names)
            validate_groups(groups)
            for group in groups:
                run_group_command(group, skip, 'reset', timestamp=timestamp)
            return

        projects = filter_projects_on_project_names(self.groups, project_names)
        validate_projects(projects)
        for project in projects:
            run_project_command(project, skip, 'reset', timestamp=timestamp)

    def sync(self, project_names, rebase=False, parallel=False):
        """Sync projects

        :param list(str) project_names: Project names to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes.
            Defaults to False
        :param Optional[bool] parallel: Whether command is being run in parallel, affects output.
            Defaults to False
        """

        projects = filter_projects_on_project_names(self.groups, project_names)
        if parallel:
            self._sync_parallel(projects, rebase=rebase)
            return

        for project in projects:
            project.sync(rebase=rebase)

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

    def _load_yaml(self):
        """Load clowder.yaml"""
        yaml = load_yaml(self.root_directory)

        self.defaults = yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in yaml['sources']]
        for group in yaml['groups']:
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))

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
            groups = filter_groups(self.groups, group_names)
            validate_groups(groups)
            projects = filter_projects_on_group_names(self.groups, group_names)
            print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = filter_projects_on_project_names(self.groups, project_names)
        validate_projects(projects)
        print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    @staticmethod
    def _sync_parallel(projects, rebase=False):
        """Sync projects in parallel

        :param list(Project) projects: Projects to sync
        :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes. Defaults to False
        """

        print(' - Sync forks in parallel\n')
        print_parallel_projects_output(projects, [])

        for project in projects:
            result = __clowder_pool__.apply_async(sync_project, args=(project, rebase), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))


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
