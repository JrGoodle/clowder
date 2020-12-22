"""Clowder command line yaml controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import BoolArgument, Subcommand
from pygoodle.console import CONSOLE

from pygoodle.yaml import yaml_string

from clowder.controller import CLOWDER_CONTROLLER, valid_clowder_yaml_required


class YamlCommand(Subcommand):
    class Meta:
        name = 'yaml'
        help = 'Print clowder yaml file information'
        args = [
            BoolArgument('--resolved', '-r', help='print resolved clowder yaml file')
        ]

    @valid_clowder_yaml_required
    def run(self, args) -> None:
        if args.resolved:
            CLOWDER_CONTROLLER.validate_projects_state(CLOWDER_CONTROLLER.projects, allow_missing=False)
            output = yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)).rstrip()
            CONSOLE.stdout(output)
        else:
            output = yaml_string(CLOWDER_CONTROLLER.get_yaml()).rstrip()
            CONSOLE.stdout(output)
