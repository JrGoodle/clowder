"""Clowder command line status controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

# from typing import Tuple

from pygoodle.app import BoolArgument, Subcommand
# from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
import clowder.util.parallel as parallel
from clowder.controller import (
    ClowderRepo,
    CLOWDER_CONTROLLER,
    # ProjectRepo,
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

        CONSOLE.enqueue_stdout(fmt.clowder_name(CLOWDER_CONTROLLER.name), newline=True)
        if args.fetch:
            clowder_repo = None
            if ENVIRONMENT.clowder_git_repo_dir is not None:
                clowder_repo = ClowderRepo(ENVIRONMENT.clowder_git_repo_dir)
            parallel.fetch(projects, clowder_repo)
        if ENVIRONMENT.clowder_repo_dir is not None:
            CONSOLE.enqueue_stdout(ClowderRepo(ENVIRONMENT.clowder_repo_dir).status, newline=True)

        project_names = CLOWDER_CONTROLLER.get_formatted_project_names(projects)
        padding = len(max(project_names, key=len))

        CONSOLE.enqueue_stdout(parallel.status(projects, padding))
        CONSOLE.flush_stdout()
