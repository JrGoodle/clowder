# -*- coding: utf-8 -*-
"""Clowder parallel command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import multiprocessing as mp
import os
import signal
from typing import List, Optional, Tuple

import psutil
from termcolor import cprint

import clowder.util.formatting as fmt
from clowder import LOG_DEBUG
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.error import ClowderError, ClowderErrorType
from clowder.model import Project

from .progress import Progress

if os.name == "posix":

    __clowder_results__ = []
    __clowder_pool__: Optional[mp.Pool] = None
    __clowder_progress__: Optional[Progress] = None
    __clowder_parent_id__ = os.getpid()

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

    def async_callback(val) -> None: # noqa
        """Increment async progress bar

        :param val: Dummy parameter to satisfy callback interface
        """

        del val
        __clowder_progress__.update()

    def worker_init() -> None:
        """
        Process pool terminator

        .. note:: Implementation source https://stackoverflow.com/a/45259908
        """

        def sig_int(signal_num, frame) -> None: # noqa
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

    def forall_parallel(commands: List[str], projects: Tuple[Project, ...], ignore_errors: bool) -> None:
        """Runs command or script for projects in parallel

        :param List[str] commands: Command to run
        :param Tuple[Project, ...] projects: Projects to run command for
        :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
        """

        print(' - Run forall commands in parallel\n')
        for project in projects:
            print(project.status())
            if not project.full_path().is_dir():
                cprint(" - Project is missing", 'red')

        for cmd in commands:
            print('\n' + fmt.command(cmd))

        global __clowder_pool__
        __clowder_pool__ = mp.Pool(initializer=worker_init)
        global __clowder_progress__
        __clowder_progress__ = Progress()

        for project in projects:
            result = __clowder_pool__.apply_async(run_project, args=(project, commands, ignore_errors),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def herd_parallel(projects: Tuple[Project, ...], branch: Optional[str] = None,
                      tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False) -> None:
        """Clone projects or update latest from upstream in parallel

        :param Tuple[Project, ...] projects: Projects to herd
        :param Optional[str] branch: Branch to attempt to herd
        :param Optional[str] tag: Tag to attempt to herd
        :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        """

        print(' - Herd projects in parallel\n')
        CLOWDER_CONTROLLER.validate_print_output(projects)

        global __clowder_pool__
        __clowder_pool__ = mp.Pool(initializer=worker_init)
        global __clowder_progress__
        __clowder_progress__ = Progress()

        for project in projects:
            result = __clowder_pool__.apply_async(herd_project,
                                                  args=(project, branch, tag, depth, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def reset_parallel(projects: Tuple[Project, ...], timestamp_project: Optional[str] = None) -> None:
        """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

        :param Tuple[Project, ...] projects: Project names to reset
        :param Optional[str] timestamp_project: Reference project to checkout other project commit timestamps relative to # noqa
        """

        print(' - Reset projects in parallel\n')
        CLOWDER_CONTROLLER.validate_print_output(projects)

        timestamp = None
        if timestamp_project:
            timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

        global __clowder_pool__
        __clowder_pool__ = mp.Pool(initializer=worker_init)
        global __clowder_progress__
        __clowder_progress__ = Progress()

        for project in projects:
            result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    # Disable warnings shown by pylint for catching too general exception
    # pylint: disable=W0703

    def pool_handler(count: int):
        """Pool handler for finishing parallel jobs

        :param int count: Total count of projects in progress bar
        :raise ClowderError:
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
                    raise ClowderError(ClowderErrorType.PARALLEL_COMMAND_FAILED, fmt.error_parallel_command_failed())
        except Exception as err:
            __clowder_progress__.close()
            __clowder_pool__.close()
            __clowder_pool__.terminate()
            LOG_DEBUG('Pool handler exception', err)
            raise ClowderError(ClowderErrorType.PARALLEL_COMMAND_FAILED, fmt.error_parallel_command_failed())
        else:
            __clowder_progress__.complete()
            __clowder_progress__.close()
            __clowder_pool__.close()
            __clowder_pool__.join()
else:
    def forall_parallel(commands: List[str], ignore_errors: bool, projects: Tuple[Project, ...]) -> None: # noqa
        """Stub for non-posix forall parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')

    def herd_parallel(projects: Tuple[Project, ...], branch: Optional[str] = None, # noqa
                      tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False) -> None: # noqa
        """Stub for non-posix herd parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')

    def reset_parallel(projects: Tuple[Project, ...], timestamp_project: Optional[str] = None) -> None: # noqa
        """Stub for non-posix reset parallel command"""

        print(' - Parallel commands are only available on posix operating systems\n')
