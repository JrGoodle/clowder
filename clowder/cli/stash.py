"""Clowder command line stash controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.console import CONSOLE

from .util import add_parser_arguments


def add_stash_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder stash parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('stash', help='Stash current changes')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=stash)

    add_parser_arguments(parser, [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to stash changes for'))),
    ])


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def stash(args) -> None:
    """Clowder stash command private implementation"""

    if not any([p.is_dirty for p in CLOWDER_CONTROLLER.projects]):
        CONSOLE.stdout(' - No changes to stash')
        return

    projects = Config().process_projects_arg(args.projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        CONSOLE.stdout(project.status())
        project.stash()
