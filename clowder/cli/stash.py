"""Clowder command line stash controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand
from pygoodle.console import CONSOLE

from clowder.controller import (
    CLOWDER_CONTROLLER,
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.config import Config

from .util import ProjectsArgument


class StashCommand(Subcommand):
    class Meta:
        name = 'stash'
        help = 'Stash current changes'
        args = [
            ProjectsArgument('projects and groups to stash changes for')
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        if not any([p.is_dirty for p in CLOWDER_CONTROLLER.projects]):
            CONSOLE.stdout(' - No changes to stash')
            return

        projects = Config().process_projects_arg(args.projects)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        for project in projects:
            CONSOLE.stdout(project.status())
            project.stash()
