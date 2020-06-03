# -*- coding: utf-8 -*-
"""Clowder command line clean controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.model import Project
from clowder.model.util import filter_projects
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_clean_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder clean parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to clean'))),
        (['--recursive', '-r'], dict(action='store_true', help='clean submodules recursively'))
    ]

    parser = subparsers.add_parser('clean', help='Discard current changes in projects')
    parser.formatter_class = argparse.RawTextHelpFormatter
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


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def clean(args) -> None:
    """Clowder clean command private implementation"""

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(args.projects)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if args.all:
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
    _clean_impl(projects, clean_args=clean_args, recursive=args.recursive)


def _clean_impl(projects: Tuple[Project, ...], clean_args: str = '', recursive: bool = False) -> None:
    """Discard changes

    :param Tuple[Project, ...] projects: Projects to clean
    :param str clean_args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool recursive: Clean submodules recursively
    """

    for project in projects:
        print(project.status())
        project.clean(args=clean_args, recursive=recursive)
