"""Clowder command line config controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

from clowder.clowder_controller import print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config, print_config


class ConfigSetJobsCommand(Subcommand):

    name = 'jobs'
    help = 'Set default number of jobs for relevant commands'
    args = [
        Argument(
            'jobs',
            metavar='<n>',
            nargs=1,
            default=None,
            type=int,
            help='Set default number of jobs to use running commands in parallel'
        )
    ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_config
    def run(self, args) -> None:
        CONSOLE.stdout(' - Set jobs config value')
        config = Config()
        config.jobs = args.jobs[0]
        config.save()
