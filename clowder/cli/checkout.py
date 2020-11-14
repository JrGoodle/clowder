"""Clowder command line checkout controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.console import CONSOLE
from clowder.data.util import filter_projects
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_checkout_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder checkout parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='<branch>')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to checkout branches for')))
    ]

    parser = subparsers.add_parser('checkout', help='Checkout local branch in projects')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=checkout)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def checkout(args) -> None:
    """Clowder checkout command private implementation"""

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        CONSOLE.stdout(project.status())
        project.checkout(args.branch[0])
