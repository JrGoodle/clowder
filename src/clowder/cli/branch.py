# -*- coding: utf-8 -*-
"""Clowder command line branch controller

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


def add_branch_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*', choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to show branches for')))
    ]

    parser = subparsers.add_parser('branch', help='Display current branches')
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=branch)


def branch(args) -> None:
    """Clowder branch command entry point"""
    _branch(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _branch(args) -> None:
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

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
    for project in projects:
        print(project.status())
        project.branch(local=local, remote=remote)
