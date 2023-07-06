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

from ...util import JobsArgument


class ConfigSetJobsCommand(Subcommand):
    class Meta:
        name = 'jobs'
        help = 'Set default number of jobs for relevant commands'
        args = [
            JobsArgument(
                positional=True,
                # help='Set default number of jobs to use running commands in parallel'
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
