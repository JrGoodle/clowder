# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import List, Optional

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    validate_project_statuses
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel import reset_parallel


def add_reset_parser(subparsers: argparse._SubParsersAction): # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.options_help_message(CLOWDER_CONTROLLER.project_choices,
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


@network_connection_required
@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status_fetch
def reset(args) -> None:
    """Clowder reset command private implementation"""

    timestamp_project = None
    if args.timestamp:
        timestamp_project = args.timestamp[0]
    _reset_impl(args.projects, timestamp_project=timestamp_project, parallel=args.parallel)


def _reset_impl(project_names: List[str], timestamp_project: Optional[str] = None, parallel: bool = False) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD

    :param List[str] project_names: Project names to reset
    :param Optional[str] timestamp_project: Reference project to checkout other project commit timestamps relative to
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)

    parallel_config = config.current_clowder_config.parallel
    parallel = parallel_config if parallel_config is not None else parallel

    projects = config.process_projects_arg(project_names)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if parallel:
        reset_parallel(projects, timestamp_project=timestamp_project)
        if os.name == "posix":
            return

    timestamp = None
    if timestamp_project:
        timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

    validate_project_statuses(projects)
    for project in projects:
        project.reset(timestamp=timestamp)
