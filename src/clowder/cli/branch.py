# -*- coding: utf-8 -*-
"""Clowder command line branch controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model.util import filter_projects
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_branch_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder branch parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to show branches for')))
    ]

    parser = subparsers.add_parser('branch', help='Display current branches')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=branch)


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

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        print(project.status())
        project.branch(local=local, remote=remote)
