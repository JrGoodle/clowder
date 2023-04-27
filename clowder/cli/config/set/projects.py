"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand
from pygoodle.console import CONSOLE

from clowder.controller import (
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.config import Config, print_config

from ...util import ProjectsArgument


class ConfigSetProjectsCommand(Subcommand):
    class Meta:
        name = 'projects'
        help = 'Set default projects and groups'
        args = [
            ProjectsArgument('Default projects and groups to run commands for', requires_arg=True)
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set projects config value')
        config = Config()
        config.projects = tuple(args.projects)
        config.save()
