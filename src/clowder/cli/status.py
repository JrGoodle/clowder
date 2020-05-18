# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

import clowder.clowder_repo as clowder_repo
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.model.project import Project
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required


def add_status_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to print status of'))),
        (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
    ]

    parser = subparsers.add_parser('status', help='Print project status')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=status)


def status(args) -> None:
    """Clowder status command entry point"""

    _status(args)


@valid_clowder_yaml_required
def _status(args) -> None:
    """Clowder status command private implementation"""

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)

    if args.fetch:
        _fetch_projects(projects)
    else:
        clowder_repo.print_status()

    padding = len(max(CLOWDER_CONTROLLER.get_project_paths(projects), key=len))

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
