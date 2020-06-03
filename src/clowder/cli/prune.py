# -*- coding: utf-8 -*-
"""Clowder command line prune controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from typing import List, Tuple

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.config import Config
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.model import Project
from clowder.model.util import (
    existing_branch_projects,
    filter_projects,
    validate_project_statuses
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)

from .util import add_parser_arguments


def add_prune_parser(subparsers: argparse._SubParsersAction): # noqa
    """Add clowder prune parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['branch'], dict(help='name of branch to remove', metavar='<branch>')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to prune'))),
        (['--force', '-f'], dict(action='store_true', help='force prune branches'))
    ]

    parser = subparsers.add_parser('prune', help='Prune branches')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)

    mutually_exclusive_arguments = [
        (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='prune remote branches'))
    ]
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    add_parser_arguments(mutually_exclusive_group, mutually_exclusive_arguments)

    parser.set_defaults(func=prune)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def prune(args) -> None:
    """Clowder prune command private implementation"""

    if args.all:
        _prune_all(args)
        return

    if args.remote:
        _prune_remote(args)
        return

    _prune_impl(args.projects, args.branch, force=args.force, local=True)


@network_connection_required
def _prune_all(args) -> None:
    """clowder prune all command"""

    _prune_impl(args.projects, args.branch, force=args.force, local=True, remote=True)


@network_connection_required
def _prune_remote(args) -> None:
    """clowder prune remote command"""

    _prune_impl(args.projects, args.branch, remote=True)


def _prune_impl(project_names: List[str], branch: str, force: bool = False,
                local: bool = False, remote: bool = False) -> None:
    """Prune branches

    :param List[str] project_names: Project names to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    """

    config = Config(CLOWDER_CONTROLLER.name, CLOWDER_CONTROLLER.project_choices)
    projects = config.process_projects_arg(project_names)
    projects = filter_projects(CLOWDER_CONTROLLER.projects, projects)

    validate_project_statuses(projects)
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
    except ClowderError as err:
        LOG_DEBUG('Invalid projects branch state', err)
        print(err)
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
            raise ClowderError(ClowderErrorType.PRUNE_NO_BRANCHES, f' - No local or remote branches to prune')
        print(' - Prune local and remote branches\n')
        return

    if remote:
        if not remote_branch_exists:
            raise ClowderError(ClowderErrorType.PRUNE_NO_BRANCHES, f' - No remote branches to prune')
        print(' - Prune remote branches\n')
        return

    if not local_branch_exists:
        raise ClowderError(ClowderErrorType.PRUNE_NO_BRANCHES, f' - No local branches to prune')
    print(' - Prune local branches\n')
