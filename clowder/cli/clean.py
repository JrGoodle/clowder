"""Clowder command line clean controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status

from .util import ProjectsArgument


class CleanCommand(Subcommand):

    name = 'clean'
    help = 'Discard current changes in projects'
    args = [
        ProjectsArgument('projects and groups to clean'),
        Argument('--recursive', '-r', action='store_true', help='clean submodules recursively')
    ]
    argument_groups = {
        'clean options': [
            Argument('--all', '-a', action='store_true', help='clean all the things'),
            Argument('-d', action='store_true', help='remove untracked directories'),
            Argument('-f', action='store_true', help='remove directories with .git subdirectory or file'),
            Argument('-X', action='store_true', help='remove only files ignored by git'),
            Argument('-x', action='store_true', help='remove all untracked files')
        ]
    }

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
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

        for project in projects:
            CONSOLE.stdout(project.status())
            project.clean(args=clean_args, submodules=args.recursive)
