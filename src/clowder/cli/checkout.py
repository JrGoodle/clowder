# -*- coding: utf-8 -*-
"""Clowder command line checkout controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


def add_checkout_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='BRANCH')),
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to checkout branches for')))
    ]

    parser = subparsers.add_parser('checkout', help='Checkout local branch in projects')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=checkout)


def checkout(args) -> None:
    """Clowder checkout command entry point"""

    _checkout(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _checkout(args) -> None:
    """Clowder checkout command private implementation"""

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
    for project in projects:
        print(project.status())
        project.checkout(args.branch[0])
