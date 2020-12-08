"""Clowder command line checkout controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status

from .util import ProjectsArgument


class CheckoutCommand(Subcommand):
    class Meta:
        name = 'checkout'
        help = 'Checkout local branch in projects'
        args = [
            Argument('branch', nargs=1, help='branch to checkout'),
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
