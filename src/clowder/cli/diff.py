# -*- coding: utf-8 -*-
"""Clowder command line diff controller

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


def add_diff_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to show diff for'))),
    ]

    parser = subparsers.add_parser('diff', help='Show git diff for projects')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=diff)


def diff(args) -> None:
    """Clowder diff command entry point"""

    _diff(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _diff(args) -> None:
    """Clowder diff command private implementation"""

    projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
    for project in projects:
        print(project.status())
        project.diff()
