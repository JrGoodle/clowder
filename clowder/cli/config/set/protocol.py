"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import SingleArgument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.clowder_controller import print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config
from clowder.git import GitProtocol


class ConfigSetProtocolCommand(Subcommand):
    class Meta:
        name = 'protocol'
        help = 'Set default git protocol'
        protocol_choices = ('https', 'ssh')
        args = [
            SingleArgument('protocol', choices=protocol_choices,
                           help=fmt.options_help_message(protocol_choices, 'Default git protocol to use'))
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set protocol config value')
        config = Config()
        config.protocol = GitProtocol(args.protocol[0])
        config.save()
