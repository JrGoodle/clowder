# -*- coding: utf-8 -*-
"""Clowder command line prune controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

from termcolor import cprint

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.error import ClowderError
from clowder.model.project import Project
from clowder.util.clowder_utils import (
    add_parser_arguments,
    existing_branch_projects,
    filter_projects,
    options_help_message,
    validate_projects
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


def add_prune_parser(subparsers: argparse._SubParsersAction): # noqa

    arguments = [
        (['branch'], dict(help='name of branch to remove', metavar='BRANCH')),
        (['projects'], dict(metavar='PROJECT', default='all', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices,
                            help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                      'projects and groups to prune'))),
        (['--force', '-f'], dict(action='store_true', help='force prune branches'))
    ]

    parser = subparsers.add_parser('prune', help='Prune branches')
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='prune remote branches'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=prune)


def prune(args) -> None:
    """Clowder prune command entry point"""

    _prune(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _prune(args) -> None:
    """Clowder prune command private implementation"""

    if args.all:
        _prune_all(args)
        return

    if args.remote:
        _prune_remote(args)
        return

    _prune_impl(CLOWDER_CONTROLLER, args.projects, args.branch,
                force=args.force, local=True)


@network_connection_required
def _prune_all(args) -> None:
    """clowder prune all command"""

    _prune_impl(CLOWDER_CONTROLLER, args.projects, args.branch,
                force=args.force, local=True, remote=True)


@network_connection_required
def _prune_remote(args) -> None:
    """clowder prune remote command"""

    _prune_impl(CLOWDER_CONTROLLER, args.projects, args.branch, remote=True)


def _prune_impl(clowder: ClowderController, project_names: Tuple[str, ...], branch: str, force: bool = False,
                local: bool = False, remote: bool = False) -> None:
    """Prune branches

    :param ClowderController clowder: ClowderController instance
    :param Tuple[str, ...] project_names: Project names to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    """

    projects = filter_projects(clowder.projects, project_names)
    validate_projects(projects)
    _prune_projects(projects, branch, force=force, local=local, remote=remote)


def _prune_projects(projects: Tuple[Project, ...], branch: str, force: bool = False, local: bool = False,
                    remote: bool = False) -> None:
    """Prune project branches

    :param Tuple[Project, ...] projects: Projects to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    """

    local_branch_exists = existing_branch_projects(projects, branch, is_remote=False)
    remote_branch_exists = existing_branch_projects(projects, branch, is_remote=True)

    try:
        _validate_branches(local, remote, local_branch_exists, remote_branch_exists)
    except ClowderError:
        pass
    else:
        for project in projects:
            print(project.status())
            project.prune(branch, force=force, local=local, remote=remote)


def _validate_branches(local: bool, remote: bool, local_branch_exists: bool, remote_branch_exists: bool) -> None:
    """Prune project branches

    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param bool local_branch_exists: Whether a local branch exists
    :param bool remote_branch_exists: Whether a remote branch exists
    :raise ClowderError:
    """

    if local and remote:
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune local and remote branches\n')
        return

    if remote:
        if not remote_branch_exists:
            cprint(' - No remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune remote branches\n')
        return

    if not local_branch_exists:
        print(' - No local branches to prune\n')
        raise ClowderError
    print(' - Prune local branches\n')
