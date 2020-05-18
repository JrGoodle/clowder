# -*- coding: utf-8 -*-
"""Clowder command line clean controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


def add_clean_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to clean'))),
        (['--recursive', '-r'], dict(action='store_true', help='clean submodules recursively'))
    ]

    parser = subparsers.add_parser('clean', help='Discard current changes in projects')
    add_parser_arguments(parser, arguments)

    options_arguments = [
        (['--all', '-a'], dict(action='store_true', help='clean all the things')),
        (['-d'], dict(action='store_true', help='remove untracked directories')),
        (['-f'], dict(action='store_true', help='remove directories with .git subdirectory or file')),
        (['-X'], dict(action='store_true', help='remove only files ignored by git')),
        (['-x'], dict(action='store_true', help='remove all untracked files'))
    ]
    options_group = parser.add_argument_group(title='clean options')
    add_parser_arguments(options_group, options_arguments)

    parser.set_defaults(func=clean)


def clean(args) -> None:
    """Clowder clean command entry point"""

    _clean(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _clean(args) -> None:
    """Clowder clean command private implementation"""

    if args.all:
        projects = filter_projects(CLOWDER_CONTROLLER.projects, args.projects)
        for project in projects:
            print(project.status())
            project.clean_all()
        return

    clean_args = ''
    if args.d:
        clean_args += 'd'
    if args.f:
        clean_args += 'f'
    if args.X:
        clean_args += 'X'
    if args.x:
        clean_args += 'x'
    _clean_impl(CLOWDER_CONTROLLER, args.projects, clean_args=clean_args, recursive=args.recursive)


def _clean_impl(clowder: ClowderController, project_names: Tuple[str, ...],
                clean_args: str = '', recursive: bool = False) -> None:
    """Discard changes

    :param ClowderController clowder: ClowderController instance
    :param Tuple[str, ...] project_names: Project names to clean
    :param str clean_args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool recursive: Clean submodules recursively
    """

    projects = filter_projects(clowder.projects, project_names)
    for project in projects:
        print(project.status())
        project.clean(args=clean_args, recursive=recursive)
