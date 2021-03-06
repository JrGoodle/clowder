"""Clowder command line prune controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
from typing import List, Tuple

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.data import ResolvedProject
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.connectivity import network_connection_required
from clowder.util.console import CONSOLE
from clowder.util.error import CommandArgumentError

from .util import add_parser_arguments


def add_prune_parser(subparsers: argparse._SubParsersAction):  # noqa
    """Add clowder prune parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('prune', help='Prune branches')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=prune)

    add_parser_arguments(parser, [
        (['branch'], dict(help='name of branch to remove', metavar='<branch>')),
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to prune'))),
        (['--force', '-f'], dict(action='store_true', help='force prune branches'))
    ])

    mutually_exclusive_arguments = [
        (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='prune remote branches'))
    ]
    add_parser_arguments(parser.add_mutually_exclusive_group(), [
        (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
        (['--remote', '-r'], dict(action='store_true', help='prune remote branches'))
    ])


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

    projects = Config().process_projects_arg(project_names)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    CLOWDER_CONTROLLER.validate_project_statuses(projects)
    _prune_projects(projects, branch, force=force, local=local, remote=remote)


def _prune_projects(projects: Tuple[ResolvedProject, ...], branch: str, force: bool = False, local: bool = False,
                    remote: bool = False) -> None:
    """Prune project branches

    :param Tuple[Project, ...] projects: Projects to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :raise CommandArgumentError:
    """

    local_branch_exists = CLOWDER_CONTROLLER.project_has_branch(projects, branch, is_remote=False)
    remote_branch_exists = CLOWDER_CONTROLLER.project_has_branch(projects, branch, is_remote=True)

    if local and remote:
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            CONSOLE.stdout(' - No local or remote branches to prune')
            return
        CONSOLE.stdout(' - Prune local and remote branches\n')
    elif remote:
        if not remote_branch_exists:
            CONSOLE.stdout(' - No remote branches to prune')
            return
        CONSOLE.stdout(' - Prune remote branches\n')
    elif local:
        if not local_branch_exists:
            CONSOLE.stdout(' - No local branches to prune')
            return
        CONSOLE.stdout(' - Prune local branches\n')
    else:
        raise CommandArgumentError('local and remote are both false, but at least one should be true')

    for project in projects:
        CONSOLE.stdout(project.status())
        project.prune(branch, force=force, local=local, remote=remote)
