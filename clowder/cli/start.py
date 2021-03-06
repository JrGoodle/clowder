"""Clowder command line start controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.connectivity import network_connection_required
from clowder.util.console import CONSOLE

from .util import add_parser_arguments


def add_start_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder start parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('start', help='Start a new branch')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=start)

    add_parser_arguments(parser, [
        (['branch'], dict(help='name of branch to create', nargs=1, default=None, metavar='<branch>')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to start branches for'))),
        (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch'))
    ])


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

    projects = Config().process_projects_arg(args.projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    CLOWDER_CONTROLLER.validate_project_statuses(projects)
    for project in projects:
        CONSOLE.stdout(project.status())
        project.start(args.branch[0], tracking)
