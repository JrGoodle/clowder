# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.clowder_repo as clowder_repo
from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import add_parser_arguments
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required


def add_status_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
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

    if args.fetch:
        _fetch_projects(CLOWDER_CONTROLLER)
    else:
        clowder_repo.print_status()

    padding = len(max(CLOWDER_CONTROLLER.get_all_project_paths(), key=len))

    for project in CLOWDER_CONTROLLER.projects:
        print(project.status(padding=padding))


@network_connection_required
def _fetch_projects(clowder: ClowderController) -> None:
    """fetch all projects

    :param ClowderController clowder: ClowderController instance
    """

    clowder_repo.print_status(fetch=True)

    print(' - Fetch upstream changes for projects\n')
    for project in clowder.projects:
        print(project.status())
        project.fetch_all()
