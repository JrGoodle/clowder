"""Clowder command line branch controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status

from .util import ProjectsArgument


class BranchCommand(Subcommand):

    name = 'branch'
    help = 'Display current branches'
    args = [
        ProjectsArgument('projects and groups to show branches for')
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
