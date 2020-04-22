# -*- coding: utf-8 -*-
"""Clowder parallel commands

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import multiprocessing as mp
import os
import signal
from typing import List, Optional

import psutil
from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.clowder_controller import ClowderController
from clowder.error.clowder_exit import ClowderExit
from clowder.model.project import Project
from clowder.util.progress import Progress
from clowder.util.clowder_utils import (
    filter_projects,
    print_parallel_projects_output
)

if os.name == "posix":
    def herd_project(project: Project, branch: str, tag: str, depth: int, rebase: bool) -> None:
        """Herd command wrapper function for multiprocessing Pool execution

        :param Project project: Project instance
        :param str branch: Branch to attempt to herd
        :param str tag: Tag to attempt to herd
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, parallel=True)

    def reset_project(project: Project, timestamp: str) -> None:
        """Reset command wrapper function for multiprocessing Pool execution

        :param Project project: Project instance
        :param str timestamp: If not None, reset to commit at timestamp, or closest previous commit
        """

        project.reset(timestamp=timestamp, parallel=True)

    def run_project(project: Project, commands: List[str], ignore_errors: bool) -> None:
        """Run command wrapper function for multiprocessing Pool execution

        :param Project project: Project instance
        :param list[str] commands: Commands to run
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        """

        project.run(commands, ignore_errors, parallel=True)

    def sync_project(project: Project, rebase: bool) -> None:
        """Sync command wrapper function for multiprocessing Pool execution

        :param Project project: Project instance
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        project.sync(rebase, parallel=True)

    def async_callback(val) -> None:
        """Increment async progress bar

        :param val: Dummy parameter to satisfy callback interface
        """

        del val
        __clowder_progress__.update()

    __clowder_parent_id__ = os.getpid()

    def worker_init() -> None:
        """
        Process pool terminator

        .. note:: Implementation source https://stackoverflow.com/a/45259908
        """

        def sig_int(signal_num, frame) -> None:
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

    def forall_parallel(commands: List[str], skip: List[str], ignore_errors: bool, projects: List[Project]) -> None:
        """Runs command or script for projects in parallel

        :param List[str] commands: Command to run
        :param List[str] skip: Project names to skip
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        :param List[Project] projects: Projects to run command for
        """

        print(' - Run forall commands in parallel\n')
        for project in projects:
            if project.name in skip:
                continue
            print(project.status())
            if not os.path.isdir(project.full_path()):
                cprint(" - Project is missing", 'red')

        for cmd in commands:
            print('\n' + fmt.command(cmd))

        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(run_project, args=(project, commands, ignore_errors),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def herd_parallel(clowder: ClowderController, group_names: List[str], branch: Optional[str] = None,
                      tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False,
                      project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
        """Clone projects or update latest from upstream in parallel

        .. py:function:: herd_parallel(clowder, group_names, branch=None, tag=None, depth=0, rebase=False, project_names=None, skip=[], protocol=None)

        :param ClowderController clowder: ClowderController instance
        :param list[str] group_names: Group names to herd
        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :param Optional[List[str]] project_names: Project names to herd
        :param Optional[List[str]] skip: Project names to skip
        """

        skip = [] if skip is None else skip

        print(' - Herd projects in parallel\n')
        clowder.validate_print_output(group_names, project_names=project_names, skip=skip)

        projects = filter_projects(clowder.groups, group_names=group_names, project_names=project_names)

        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(herd_project,
                                                  args=(project, branch, tag, depth, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def reset_parallel(clowder: ClowderController, group_names: List[str], timestamp_project: Optional[str] = None,
                       project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
        """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

        .. py:function:: reset_parallel(clowder, group_names, timestamp_project=None, project_names=None, skip=[])

        :param ClowderController clowder: ClowderController instance
        :param List[str] group_names: Group names to reset
        :param Optional[str] timestamp_project: Reference project to checkout commit timestamps of other projects relative to
        :param Optional[List[str]] project_names: Project names to reset
        :param Optional[List[str]] skip: Project names to skip
        """

        skip = [] if skip is None else skip

        print(' - Reset projects in parallel\n')
        timestamp = None
        if timestamp_project:
            timestamp = clowder.get_timestamp(timestamp_project)

        clowder.validate_print_output(group_names, project_names=project_names, skip=skip)

        projects = filter_projects(clowder.groups, group_names=group_names, project_names=project_names)

        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    def sync_parallel(projects: List[Project], rebase: bool = False) -> None:
        """Sync projects in parallel

        :param list[Project] projects: Projects to sync
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        print(' - Sync forks in parallel\n')
        print_parallel_projects_output(projects, [])

        for project in projects:
            result = __clowder_pool__.apply_async(sync_project, args=(project, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    # Disable warnings shown by pylint for catching too general exception
    # pylint: disable=W0703

    def pool_handler(count: int):
        """Pool handler for finishing parallel jobs

        :param int count: Total count of projects in progress bar
        :raise ClowderExit:
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
                    raise ClowderExit(1)
        except Exception as err:
            __clowder_progress__.close()
            __clowder_pool__.close()
            __clowder_pool__.terminate()
            cprint('\n' + str(err) + '\n', 'red')
            raise ClowderExit(1)
        else:
            __clowder_progress__.complete()
            __clowder_progress__.close()
            __clowder_pool__.close()
            __clowder_pool__.join()
else:
    def forall_parallel(commands: List[str], skip: List[str], ignore_errors: bool, projects: List[Project]) -> None:
        """Stub for non-posix forall parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')

    def herd_parallel(clowder: ClowderController, group_names: List[str], branch: Optional[str] = None,
                      tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False,
                      project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
        """Stub for non-posix herd parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')

    def reset_parallel(clowder: ClowderController, group_names: List[str], timestamp_project: Optional[str] = None,
                       project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
        """Stub for non-posix reset parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')

    def sync_parallel(projects: List[Project], rebase: bool = False) -> None:
        """Stub for non-posix sync parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')
