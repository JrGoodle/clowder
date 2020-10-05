# -*- coding: utf-8 -*-
"""Clowder command line yaml controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.data.util import validate_project_statuses
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.yaml import yaml_string

from .util import add_parser_arguments


def add_yaml_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder yaml parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder yaml file'))
    ]

    parser = subparsers.add_parser('yaml', help='Print clowder yaml file information')
    parser.formatter_class = argparse.RawTextHelpFormatter
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=yaml)


@valid_clowder_yaml_required
def yaml(args) -> None:
    """Clowder yaml command private implementation"""

    if args.resolved:
        validate_project_statuses(CLOWDER_CONTROLLER.projects, allow_missing_repo=False)
        output = yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)).rstrip()
        print(output)
    else:
        output = yaml_string(CLOWDER_CONTROLLER.get_yaml()).rstrip()
        print(output)
