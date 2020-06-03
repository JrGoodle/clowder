# -*- coding: utf-8 -*-
"""Clowder command line stash controller

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


def add_stash_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder stash parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to stash changes for'))),
    ]

    parser = subparsers.add_parser('stash', help='Stash current changes')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=stash)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def stash(args) -> None:
    """Clowder stash command private implementation"""

    if not any([p.is_dirty() for p in CLOWDER_CONTROLLER.projects]):
        print(' - No changes to stash')
        return

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    for project in projects:
        print(project.status())
        project.stash()
