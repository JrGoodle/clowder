# -*- coding: utf-8 -*-
"""Clowder command line stash controller

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


def add_stash_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to stash changes for'))),
    ]

    parser = subparsers.add_parser('stash', help='Stash current changes')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=stash)


def stash(args) -> None:
    """Clowder stash command entry point"""

    _stash(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _stash(args) -> None:
    """Clowder stash command private implementation"""

    if not any([p.is_dirty() for p in CLOWDER_CONTROLLER.projects]):
        print('No changes to stash')
        return

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
    for project in projects:
        print(project.status())
        project.stash()
