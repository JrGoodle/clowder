"""Clowder command line checkout controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import SingleArgument, Subcommand
from clowder.util.console import CONSOLE

from clowder.controller import (
    CLOWDER_CONTROLLER,
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.config import Config

from .util import ProjectsArgument


class CheckoutCommand(Subcommand):
    class Meta:
        name = 'checkout'
        help = 'Checkout local branch in projects'
        args = [
            SingleArgument('branch', help='branch to checkout'),
            ProjectsArgument('projects and groups to checkout branches for')
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        for project in projects:
            CONSOLE.stdout(project.status())
            project.checkout(args.branch[0])
