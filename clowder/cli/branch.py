"""Clowder command line branch controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.console import CONSOLE

from .util import add_parser_arguments


def add_branch_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder branch parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('branch', help='Display current branches')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=branch)

    add_parser_arguments(parser, [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to show branches for')))
    ])

    add_parser_arguments(parser.add_mutually_exclusive_group(), [
        (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
    ])


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def branch(args) -> None:
    """Clowder branch command private implementation"""

    if args.remote:
        local = False
        remote = True
    elif args.all:
        local = True
        remote = True
    else:
        local = True
        remote = False

    projects = Config().process_projects_arg(args.projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        CONSOLE.stdout(project.status())
        project.branch(local=local, remote=remote)
