"""Clowder command line clean controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
from typing import Tuple

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.data import ResolvedProject
from clowder.git.clowder_repo import print_clowder_repo_status


class CleanCommand(Subcommand):

    name = 'clean'
    help = 'Discard current changes in projects'
    args = [
        Argument(
            'projects',
            metavar='<project|group>',
            default='default',
            nargs='*',
            choices=CLOWDER_CONTROLLER.project_choices_with_default,
            help=fmt.project_options_help_message('projects and groups to clean')
        )
    ]
    mutually_exclusive_args = [
        [
            Argument('--all', '-a', action='store_true', help='show local and remote branches'),
            Argument('--remote', '-r', action='store_true', help='show local and remote branches')
        ]
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        if args.remote:
            local = False
            remote = True
        elif args.all:
            local = True
            remote = True
        else:
            local = True
            remote = False

        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        for project in projects:
            CONSOLE.stdout(project.status())
            project.branch(local=local, remote=remote)


def add_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder clean parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('clean', help='Discard current changes in projects')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=clean)

    add_parser_arguments(parser, [
        (['projects'], dict(metavar='<project|group>', default='default', nargs='*',
                            choices=CLOWDER_CONTROLLER.project_choices_with_default,
                            help=fmt.project_options_help_message('projects and groups to clean'))),
        (['--recursive', '-r'], dict(action='store_true', help='clean submodules recursively'))
    ])

    add_parser_arguments(parser.add_argument_group(title='clean options'), [
        (['--all', '-a'], dict(action='store_true', help='clean all the things')),
        (['-d'], dict(action='store_true', help='remove untracked directories')),
        (['-f'], dict(action='store_true', help='remove directories with .git subdirectory or file')),
        (['-X'], dict(action='store_true', help='remove only files ignored by git')),
        (['-x'], dict(action='store_true', help='remove all untracked files'))
    ])


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def clean(args) -> None:
    """Clowder clean command private implementation"""

    projects = Config().process_projects_arg(args.projects)
    projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

    if args.all:
        for project in projects:
            CONSOLE.stdout(project.status())
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
    _clean_impl(projects, clean_args=clean_args, submodules=args.recursive)


def _clean_impl(projects: Tuple[ResolvedProject, ...], clean_args: str = '', submodules: bool = False) -> None:
    """Discard changes

    :param Tuple[Project, ...] projects: Projects to clean
    :param str clean_args: Git clean options
        - ``d`` Remove untracked directories in addition to untracked files
        - ``f`` Delete directories with .git sub directory or file
        - ``X`` Remove only files ignored by git
        - ``x`` Remove all untracked files
    :param bool submodules: Clean submodules recursively
    """

    for project in projects:
        CONSOLE.stdout(project.status())
        project.clean(args=clean_args, submodules=submodules)
