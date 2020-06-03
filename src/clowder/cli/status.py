# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model import Project
from clowder.model.util import filter_projects
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_status_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder status parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to print status of'))),
        (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
    ]

    parser = subparsers.add_parser('status', help='Print project status')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=status)


@valid_clowder_yaml_required
@print_clowder_name
def status(args) -> None:
    """Clowder status command private implementation"""

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if args.fetch:
        _fetch_projects(projects)
    else:
        clowder_repo.print_status()

    padding = len(max(CLOWDER_CONTROLLER.get_projects_output(projects), key=len))

    for project in projects:
        print(project.status(padding=padding))


@network_connection_required
def _fetch_projects(projects: Tuple[Project, ...]) -> None:
    """fetch all projects

    :param Tuple[Project, ...] projects: Projects to fetch
    """

    clowder_repo.print_status(fetch=True)

    print(' - Fetch upstream changes for projects\n')
    for project in projects:
        print(project.status())
        project.fetch_all()
    print()
