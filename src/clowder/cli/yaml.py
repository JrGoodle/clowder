# -*- coding: utf-8 -*-
"""Clowder command line yaml controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.decorators import (
    print_clowder_name,
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.yaml import print_yaml

from .util import add_parser_arguments


def add_yaml_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder yaml parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    arguments = [
        (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder yaml file'))
    ]

    parser = subparsers.add_parser('yaml', help='Print clowder yaml file information')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=yaml)


@valid_clowder_yaml_required
@print_clowder_name
@print_clowder_repo_status
def yaml(args) -> None:
    """Clowder yaml command private implementation"""

    if args.resolved:
        print(fmt.yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)))
    else:
        print_yaml()
