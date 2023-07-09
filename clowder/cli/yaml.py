"""Clowder command line yaml controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import BoolArgument, Subcommand
from clowder.util.console import CONSOLE

from clowder.util.yaml import Yaml

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
        output = Yaml.get_string(CLOWDER_CONTROLLER.get_yaml(resolved=args.resolved))
        CONSOLE.stdout(output)
