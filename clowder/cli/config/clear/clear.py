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

from .jobs import ConfigClearJobsCommand
from .projects import ConfigClearProjectsCommand
from .protocol import ConfigClearProtocolCommand
from .rebase import ConfigClearRebaseCommand


class ConfigClearCommand(Subcommand):
    class Meta:
        name = 'clear'
        help = 'Clear clowder config options'
        subcommands = [
            ConfigClearJobsCommand,
            ConfigClearProjectsCommand,
            ConfigClearProtocolCommand,
            ConfigClearRebaseCommand
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Clear all config values')
        config = Config()
        config.clear()
        config.save()
