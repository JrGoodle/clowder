# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import Optional, Tuple

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message,
    validate_projects
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import reset_parallel


def add_reset_parser(subparsers: argparse._SubParsersAction): # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to reset'))),
        (['--parallel', '-p'], dict(action='store_true', help='run commands in parallel')),
        (['--timestamp', '-t'], dict(choices=CLOWDER_CONTROLLER.project_names,
                                     default=None, nargs=1, metavar='TIMESTAMP',
                                     help='project to reset timestamps relative to'))
    ]

    parser = subparsers.add_parser('reset', help='Reset branches to upstream commits or '
                                                 'check out detached HEADs for tags and shas')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=reset)


def reset(args) -> None:
    """Clowder reset command entry point"""

    _reset(args)


@network_connection_required
@valid_clowder_yaml_required
@print_clowder_repo_status_fetch
def _reset(args) -> None:
    """Clowder reset command private implementation"""

    timestamp_project = None
    if args.timestamp:
        timestamp_project = args.timestamp[0]
    _reset_impl(CLOWDER_CONTROLLER, args.projects, timestamp_project=timestamp_project,
                parallel=args.parallel)


def _reset_impl(clowder: ClowderController, project_names: Tuple[str, ...], timestamp_project: Optional[str] = None,
                parallel: bool = False) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD

    :param ClowderController clowder: ClowderController instance
    :param Tuple[str, ...] project_names: Project names to reset
    :param Optional[str] timestamp_project: Reference project to checkout other project commit timestamps relative to
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    if parallel:
        reset_parallel(clowder, project_names, timestamp_project=timestamp_project)
        if os.name == "posix":
            return

    timestamp = None
    if timestamp_project:
        timestamp = clowder.get_timestamp(timestamp_project)

    projects = filter_projects(clowder.projects, project_names)
    validate_projects(projects)
    for project in projects:
        project.reset(timestamp=timestamp)
