# -*- coding: utf-8 -*-
"""Clowder command line start controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message,
    validate_projects
)


def add_start_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['branch'], dict(help='name of branch to create', nargs=1, default=None, metavar='BRANCH')),
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to start branches for'))),
        (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch'))
    ]

    parser = subparsers.add_parser('start', help='Start a new branch')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=start)


def start(args) -> None:
    """Clowder start command entry point"""

    _start(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _start(args) -> None:
    """Clowder start command private implementation"""

    if args.tracking:
        _start_tracking(args)
        return

    _start_branches(args, False)


@network_connection_required
def _start_tracking(args) -> None:
    """clowder start tracking command"""

    _start_branches(args, True)


def _start_branches(args, tracking: bool) -> None:
    """clowder start branches command

    :param bool tracking: Whether to create tracking branches
    """

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
    validate_projects(projects)
    for project in projects:
        print(project.status())
        project.start(args.branch[0], tracking)
