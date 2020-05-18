# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import List, Tuple

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import forall_parallel


def add_forall_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to run command for'))),
        (['--command', '-c'], dict(nargs='+', metavar='COMMAND', default=None,
                                   help='command or script to run in project directories')),
        (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
        (['--parallel', '-p'], dict(action='store_true', help='run commands in parallel'))
    ]

    parser = subparsers.add_parser('forall', help='Run command or script in project directories')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=forall)


def forall(args) -> None:
    """Clowder forall command entry point"""

    _forall(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _forall(args) -> None:
    """Clowder forall command private implementation"""

    _forall_impl(CLOWDER_CONTROLLER, args.command, args.ignore_errors,
                 project_names=args.projects, parallel=args.parallel)


def _forall_impl(clowder: ClowderController, command: List[str], ignore_errors: bool,
                 project_names: Tuple[str, ...], parallel: bool = False) -> None:
    """Runs script in project directories specified

    :param ClowderController clowder: ClowderController instance
    :param list[str] command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param Tuple[str, ...] project_names: Project names to clean
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    projects = filter_projects(clowder.projects, project_names)

    if parallel:
        forall_parallel([" ".join(command)], projects, ignore_errors)
        if os.name == "posix":
            return

    for project in projects:
        print(project.status())
        project.run([" ".join(command)], ignore_errors)
