# -*- coding: utf-8 -*-
"""Clowder parallel commands

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import multiprocessing as mp
import os
import signal

import psutil
from cement.core.foundation import CementApp
from termcolor import cprint

from clowder.error.clowder_exit import ClowderExit
from clowder.util.progress import Progress


def herd_project(project, branch, tag, depth, rebase, protocol):
    """Herd command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str branch: Branch to attempt to herd
    :param str tag: Tag to attempt to herd
    :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    :param str protocol: Git protocol ('ssh' or 'https')
    """

    project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, parallel=True, protocol=protocol)


def reset_project(project, timestamp):
    """Reset command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param str timestamp: If not None, reset to commit at timestamp, or closest previous commit
    """

    project.reset(timestamp=timestamp, parallel=True)


def run_project(project, commands, ignore_errors):
    """Run command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param list[str] commands: Commands to run
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    """

    project.run(commands, ignore_errors, parallel=True)


def sync_project(project, rebase):
    """Sync command wrapper function for multiprocessing Pool execution

    :param Project project: Project instance
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    project.sync(rebase, parallel=True)


__process_parent_id__ = os.getpid()


def worker_init():
    """
    Process pool terminator

    .. note:: Implementation source https://stackoverflow.com/a/45259908
    """

    def sig_int(signum, frame):
        """Signal handler

        :param signum: Dummy parameter to satisfy callback interface
        :param frame: Dummy parameter to satisfy callback interface
        """

        # Cement signal hook
        for f_global in frame.f_globals.values():
            if isinstance(f_global, CementApp):
                app = f_global
                for res in app.hook.run('signal', app, signum, frame):
                    pass

        # Terminate subprocesses
        del signum, frame
        parent = psutil.Process(__process_parent_id__)
        for child in parent.children(recursive=True):
            if child.pid != os.getpid():
                child.terminate()
        parent.terminate()
        psutil.Process(os.getpid()).terminate()
        print('\n\n')

    signal.signal(signal.SIGINT, sig_int)


# Disable warnings shown by pylint for catching too general exception
# pylint: disable=W0703


def run_parallel_command(command, projects, skip, *args):
    """Run parallel command

    :param callable command: Function to run
    :param list[Project] projects: Projects to run function for
    :param list[str] skip: Project names to skip
    :param args: Aguments to pass to function
    """

    __results__ = []
    __progress__ = Progress()
    __pool__ = mp.Pool(initializer=worker_init)

    def async_callback(val):
        """Increment async progress bar

        :param val: Dummy parameter to satisfy callback interface
        """

        del val
        __progress__.update()

    def pool_handler(count):
        """Pool handler for finishing parallel jobs

        :param int count: Total count of projects in progress bar
        :raise ClowderExit:
        """

        print()
        __progress__.start(count)

        try:
            for result in __results__:
                result.get()
                if not result.successful():
                    __progress__.close()
                    __pool__.close()
                    __pool__.terminate()
                    cprint('\n - Command failed\n', 'red')
                    raise ClowderExit(1)
        except Exception:
            __progress__.close()
            __pool__.close()
            __pool__.terminate()
            # cprint('\n' + str(err) + '\n', 'red')
            raise
        else:
            __progress__.complete()
            __progress__.close()
            __pool__.close()
            __pool__.join()

    for project in projects:
        if project.name in skip:
            continue
        parallel_args = tuple([project] + list(args))
        rslt = __pool__.apply_async(command, args=parallel_args, callback=async_callback)
        __results__.append(rslt)

    pool_handler(len(projects))

