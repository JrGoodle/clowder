# -*- coding: utf-8 -*-
"""Clowder command line herd controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os
from typing import Optional, Tuple

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    add_parser_arguments,
    filter_projects,
    options_help_message,
    validate_projects
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import herd_parallel


def add_herd_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to show branches for'))),
        (['--parallel', '-p'], dict(action='store_true', help='run commands in parallel')),
        (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
        (['--depth', '-d'], dict(default=None, type=int, nargs=1, metavar='DEPTH', help='depth to herd'))
    ]

    parser = subparsers.add_parser('herd', help='Clone and update projects with latest changes')
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--branch', '-b'], dict(nargs=1, default=None, metavar='BRANCH', help='branch to herd if present')),
        (['--tag', '-t'], dict(nargs=1, default=None, metavar='TAG', help='tag to herd if present'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=herd)


def herd(args) -> None:
    """Clowder herd command entry point"""

    _herd(args)


@network_connection_required
@valid_clowder_yaml_required
@print_clowder_repo_status_fetch
def _herd(args) -> None:
    """Clowder herd command private implementation"""

    branch = None if args.branch is None else args.branch[0]
    tag = None if args.tag is None else args.tag[0]
    depth = None if args.depth is None else args.depth[0]
    project_names = args.projects
    rebase = args.rebase

    if args.parallel:
        herd_parallel(CLOWDER_CONTROLLER, project_names, branch=branch, tag=tag, depth=depth, rebase=rebase)
        if os.name == "posix":
            return

    _herd_impl(CLOWDER_CONTROLLER, project_names, branch=branch, tag=tag, depth=depth, rebase=rebase)


def _herd_impl(clowder: ClowderController, project_names: Tuple[str, ...], branch: Optional[str] = None,
               tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False) -> None:
    """Clone projects or update latest from upstream

    :param ClowderController clowder: ClowderController instance
    :param Tuple[str, ...] project_names: Project names to herd
    :param Optional[str] branch: Branch to attempt to herd
    :param Optional[str] tag: Tag to attempt to herd
    :param Optonal[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    projects = filter_projects(clowder.projects, project_names)
    validate_projects(projects)
    for project in projects:
        print(project.status())
        project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase)
