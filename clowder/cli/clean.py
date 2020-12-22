"""Clowder command line clean controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import ArgumentGroup, BoolArgument, Subcommand
from pygoodle.console import CONSOLE

from clowder.controller import (
    CLOWDER_CONTROLLER,
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.config import Config

from .util import ProjectsArgument


class CleanCommand(Subcommand):
    class Meta:
        name = 'clean'
        help = 'Discard current changes in projects'
        args = [
            ProjectsArgument('projects and groups to clean'),
            BoolArgument('--recursive', '-r', help='clean submodules recursively')
        ]
        argument_groups = [
            ArgumentGroup(
                title='clean options',
                args=[
                    BoolArgument('--all', '-a', help='clean all the things'),
                    BoolArgument('-d', help='remove untracked directories'),
                    BoolArgument('-f', help='remove directories with .git subdirectory or file'),
                    BoolArgument('-X', help='remove only files ignored by git'),
                    BoolArgument('-x', help='remove all untracked files')
                ]
            )
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        if args.all:
            for project in projects:
                CONSOLE.stdout(project.status())
                # FIXME: Make sure this behaves as expected
                project.repo.groom()
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

        for project in projects:
            CONSOLE.stdout(project.status())
            project.clean(args=clean_args, submodules=args.recursive)
