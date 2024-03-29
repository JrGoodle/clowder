"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import Subcommand
from clowder.util.console import CONSOLE

from clowder.controller import (
    print_clowder_name,
    valid_clowder_yaml_required
)
from clowder.config import Config, print_config


class ConfigClearJobsCommand(Subcommand):
    class Meta:
        name = 'jobs'
        help = 'Clear default jobs count'

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Clear jobs config value')
        config = Config()
        config.jobs = None
        config.save()
