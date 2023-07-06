"""Clowder command line branch controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import BoolArgument, MutuallyExclusiveArgumentGroup, Subcommand
from clowder.util.console import CONSOLE

from clowder.controller import (
    CLOWDER_CONTROLLER,
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.config import Config

from .util import ProjectsArgument


class BranchCommand(Subcommand):
    class Meta:
        name = 'branch'
        help = 'Display current branches'
        args = [
            ProjectsArgument('projects and groups to show branches for')
        ]
        mutually_exclusive_args = [
            MutuallyExclusiveArgumentGroup(
                args=[
                    BoolArgument('--all', '-a', help='show local and remote branches'),
                    BoolArgument('--remote', '-r', help='show local and remote branches')
                ]
            )
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
