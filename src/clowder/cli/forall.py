# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import List, Optional

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model.util import filter_projects
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.parallel import forall_parallel

from .util import add_parser_arguments


def add_forall_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder forall parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to run command for'))),
        (['--command', '-c'], dict(nargs='+', metavar='<command>', default=None,
                                   help='command or script to run in project directories')),
        (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
        (['--jobs', '-j'], dict(metavar='<n>', nargs=1, default=None, type=int,
                                help='number of jobs to use runnning commands in parallel')),
    ]

    parser = subparsers.add_parser('forall', help='Run command or script in project directories')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=forall)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def forall(args) -> None:
    """Clowder forall command private implementation"""

    jobs = None
    if args.jobs:
        jobs = args.jobs[0]

    _forall_impl(args.command, args.ignore_errors, projects=args.projects, jobs=jobs)


def _forall_impl(command: List[str], ignore_errors: bool, projects: List[str], jobs: Optional[int] = None) -> None:
    """Runs script in project directories specified

    :param list[str] command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param List[str] projects: Project names to clean
    :param Optional[int] jobs: Number of jobs to use running parallel commands
    """

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    jobs_config = config.current_clowder_config.jobs
    jobs = jobs_config if jobs_config is not None else jobs

    if jobs is not None and jobs != 1 and os.name == "posix":
        if jobs <= 0:
            jobs = 4
        forall_parallel([" ".join(command)], projects, jobs, ignore_errors=ignore_errors)
        return

    for project in projects:
        print(project.status())
        project.run([" ".join(command)], ignore_errors=ignore_errors)
