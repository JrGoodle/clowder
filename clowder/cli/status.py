"""Clowder command line status controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.console import CONSOLE
from clowder.data import ResolvedProject
from clowder.data.util import filter_projects
from clowder.environment import ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_status_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
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
        if ENVIRONMENT.clowder_repo_dir is not None:
            ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status()

    projects_output = CLOWDER_CONTROLLER.get_projects_output(projects)
    padding = len(max(projects_output, key=len))

    for project in projects:
        CONSOLE.stdout(project.status(padding=padding))


@network_connection_required
def _fetch_projects(projects: Tuple[ResolvedProject, ...]) -> None:
    """fetch all projects

    :param Tuple[ResolvedProject, ...] projects: Projects to fetch
    """

    if ENVIRONMENT.clowder_repo_dir is not None:
        ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status(fetch=True)

    CONSOLE.stdout(' - Fetch upstream changes for projects\n')
    for project in projects:
        CONSOLE.stdout(project.status())
        project.fetch_all()
    CONSOLE.stdout()
