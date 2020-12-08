"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand

from clowder.clowder_controller import print_clowder_name, valid_clowder_yaml_required
from clowder.config import print_config

from .clear import ConfigClearCommand
from .set import ConfigSetCommand


class ConfigCommand(Subcommand):
    class Meta:
        name = 'config'
        help = 'Manage clowder config (EXPERIMENTAL)'
        subcommands = [
            ConfigClearCommand,
            ConfigSetCommand
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        pass
