"""Clowder command line status controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Tuple

from pygoodle.app import BoolArgument, Subcommand
from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE

from clowder.controller import (
    ClowderRepo,
    CLOWDER_CONTROLLER,
    print_clowder_name,
    ProjectRepo,
    valid_clowder_yaml_required
)
from clowder.config import Config
from clowder.environment import ENVIRONMENT

from .util import ProjectsArgument


class StatusCommand(Subcommand):
    class Meta:
        name = 'status'
        help = 'projects and groups to print status of'
        args = [
            ProjectsArgument('projects and groups to show diff for'),
            BoolArgument('--fetch', '-f', help='fetch projects before printing status')
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    def run(self, args) -> None:
        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        if args.fetch:
            self._fetch_projects(projects)
        else:
            if ENVIRONMENT.clowder_repo_dir is not None:
                ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status()

        projects_output = CLOWDER_CONTROLLER.get_projects_output(projects)
        padding = len(max(projects_output, key=len))

        for project in projects:
            CONSOLE.stdout(project.status(padding=padding))

    @staticmethod
    @network_connection_required
    def _fetch_projects(projects: Tuple[ProjectRepo, ...]) -> None:
        """fetch all projects

        :param Tuple[ProjectRepo, ...] projects: Projects to fetch
        """

        if ENVIRONMENT.clowder_repo_dir is not None:
            ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status(fetch=True)

        CONSOLE.stdout(' - Fetch upstream changes for projects\n')
        for project in projects:
            CONSOLE.stdout(project.status())
            project.fetch_all()
        CONSOLE.stdout()
