"""Clowder command line status controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Tuple

from pygoodle.app import BoolArgument, Subcommand
from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.controller import (
    ClowderRepo,
    CLOWDER_CONTROLLER,
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
    def run(self, args) -> None:
        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        output = [fmt.clowder_name(CLOWDER_CONTROLLER.name)]
        output += ['']
        if args.fetch:
            self._fetch_projects(projects)
        else:
            if ENVIRONMENT.clowder_repo_dir is not None:
                output += ClowderRepo(ENVIRONMENT.clowder_repo_dir).status()
                output += ['']

        project_names = CLOWDER_CONTROLLER.get_formatted_project_names(projects)
        padding = len(max(project_names, key=len))

        output += parallel.status(projects, padding)
        CONSOLE.stdout('\n'.join(output))

    @staticmethod
    @network_connection_required
    def _fetch_projects(projects: Tuple[ProjectRepo, ...]) -> None:
        """fetch all projects

        :param Tuple[ProjectRepo, ...] projects: Projects to fetch
        """

        if ENVIRONMENT.clowder_repo_dir is not None:
            CONSOLE.stdout(ClowderRepo(ENVIRONMENT.clowder_repo_dir).status(fetch=True))

        CONSOLE.stdout(' - Fetch upstream changes for projects\n')
        for project in projects:
            CONSOLE.stdout(project.status())
            project.fetch_all()
        CONSOLE.stdout()
