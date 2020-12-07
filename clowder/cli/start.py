"""Clowder command line start controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, BoolArgument, Subcommand
from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git.clowder_repo import print_clowder_repo_status

from .util import ProjectsArgument


class StartCommand(Subcommand):

    name = 'start'
    help = 'Start a new branch'
    args = [
        Argument('branch', help='name of branch to create', nargs=1, default=None),
        ProjectsArgument('projects and groups to start branches for'),
        BoolArgument('--tracking', '-t', help='create remote tracking branch')
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        if args.tracking:
            self._start_tracking(args)
            return

        self._start_branches(args, False)

    @network_connection_required
    def _start_tracking(self, args) -> None:
        """clowder start tracking command"""

        self._start_branches(args, True)

    @staticmethod
    def _start_branches(args, tracking: bool) -> None:
        """clowder start branches command

        :param bool tracking: Whether to create tracking branches
        """

        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        CLOWDER_CONTROLLER.validate_project_statuses(projects)
        for project in projects:
            CONSOLE.stdout(project.status())
            project.start(args.branch[0], tracking)
