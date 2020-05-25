# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import List

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
        (['projects'], dict(metavar='PROJECT', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.options_help_message(CLOWDER_CONTROLLER.project_choices,
                                                          'projects and groups to run command for'))),
        (['--command', '-c'], dict(nargs='+', metavar='COMMAND', default=None,
                                   help='command or script to run in project directories')),
        (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
        (['--parallel', '-p'], dict(action='store_true', help='run commands in parallel'))
    ]

    parser = subparsers.add_parser('forall', help='Run command or script in project directories')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=forall)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def forall(args) -> None:
    """Clowder forall command private implementation"""

    _forall_impl(args.command, args.ignore_errors, projects=args.projects, parallel=args.parallel)


def _forall_impl(command: List[str], ignore_errors: bool, projects: List[str], parallel: bool = False) -> None:
    """Runs script in project directories specified

    :param list[str] command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param List[str] projects: Project names to clean
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    parallel_config = config.current_clowder_config.parallel
    parallel = parallel_config if parallel_config is not None else parallel

    if parallel and os.name == "posix":
        forall_parallel([" ".join(command)], projects, ignore_errors)
        return

    for project in projects:
        print(project.status())
        project.run([" ".join(command)], ignore_errors)
