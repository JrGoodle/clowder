"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config


class ConfigSetProjectsCommand(Subcommand):

    name = 'projects'
    help = 'Set default projects and groups'
    args = [
        Argument(
            'projects',
            metavar='<project|group>',
            nargs='+',
            choices=CLOWDER_CONTROLLER.project_choices,
            help=fmt.project_options_help_message('Default projects and groups to run commands for')
        )
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set projects config value')
        config = Config()
        config.projects = tuple(args.projects)
        config.save()
