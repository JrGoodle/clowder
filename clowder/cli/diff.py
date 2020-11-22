"""Clowder command line diff controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.util.console import CONSOLE
from clowder.git.clowder_repo import print_clowder_repo_status

from .util import add_parser_arguments


def add_diff_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder diff parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to show diff for'))),
    ]

    parser = subparsers.add_parser('diff', help='Show git diff for projects')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=diff)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def diff(args) -> None:
    """Clowder diff command private implementation"""

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        CONSOLE.stdout(project.status())
        project.diff()
