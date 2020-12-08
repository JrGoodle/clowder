"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand

from .jobs import ConfigSetJobsCommand
from .projects import ConfigSetProjectsCommand
from .protocol import ConfigSetProtocolCommand
from .rebase import ConfigSetRebaseCommand


class ConfigSetCommand(Subcommand):
    class Meta:
        name = 'set'
        help = 'Set clowder config options'
        subcommands = [
            ConfigSetJobsCommand(),
            ConfigSetRebaseCommand(),
            ConfigSetProjectsCommand(),
            ConfigSetProtocolCommand()
        ]

    def run(self, args) -> None:
        self.print_help()
