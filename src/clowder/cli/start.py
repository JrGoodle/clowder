# -*- coding: utf-8 -*-
"""Clowder command line start controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model.util import (
    filter_projects,
    validate_project_statuses
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_start_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder start parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['branch'], dict(help='name of branch to create', nargs=1, default=None, metavar='<branch>')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to start branches for'))),
        (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch'))
    ]

    parser = subparsers.add_parser('start', help='Start a new branch')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=start)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def start(args) -> None:
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

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    validate_project_statuses(projects)
    for project in projects:
        print(project.status())
        project.start(args.branch[0], tracking)
