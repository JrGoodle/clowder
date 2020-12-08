"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config
from clowder.git import GitProtocol


class ConfigSetRebaseCommand(Subcommand):
    class Meta:
        name = 'rebase'
        help = 'Set use rebase with herd command'

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set rebase config value')
        config = Config()
        config.rebase = True
        config.save()
