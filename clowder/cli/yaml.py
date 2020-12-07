"""Clowder command line yaml controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, valid_clowder_yaml_required
from clowder.util.yaml import yaml_string


class YamlCommand(Subcommand):

    name = 'yaml'
    help = 'Print clowder yaml file information'
    args = [
        Argument('--resolved', '-r', action='store_true', help='print resolved clowder yaml file')
    ]

    @valid_clowder_yaml_required
    def run(self, args) -> None:
        if args.resolved:
            CLOWDER_CONTROLLER.validate_project_statuses(CLOWDER_CONTROLLER.projects, allow_missing_repo=False)
            output = yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)).rstrip()
            CONSOLE.stdout(output)
        else:
            output = yaml_string(CLOWDER_CONTROLLER.get_yaml()).rstrip()
            CONSOLE.stdout(output)
