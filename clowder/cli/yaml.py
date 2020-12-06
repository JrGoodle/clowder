"""Clowder command line yaml controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

from pygoodle.cli import add_parser_arguments
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, valid_clowder_yaml_required
from clowder.util.yaml import yaml_string


def add_yaml_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder yaml parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('yaml', help='Print clowder yaml file information')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=yaml)

    add_parser_arguments(parser, [
        (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder yaml file'))
    ])


@valid_clowder_yaml_required
def yaml(args) -> None:
    """Clowder yaml command private implementation"""

    if args.resolved:
        CLOWDER_CONTROLLER.validate_project_statuses(CLOWDER_CONTROLLER.projects, allow_missing_repo=False)
        output = yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)).rstrip()
        CONSOLE.stdout(output)
    else:
        output = yaml_string(CLOWDER_CONTROLLER.get_yaml()).rstrip()
        CONSOLE.stdout(output)
