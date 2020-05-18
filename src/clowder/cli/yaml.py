# -*- coding: utf-8 -*-
"""Clowder command line yaml controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.clowder_utils import add_parser_arguments
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.yaml import print_yaml


def add_yaml_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder.yaml'))
    ]

    parser = subparsers.add_parser('yaml', help='Print clowder.yaml information')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=yaml)


def yaml(args) -> None:
    """Clowder yaml command entry point"""

    _yaml(args)


@valid_clowder_yaml_required
@print_clowder_repo_status
def _yaml(args) -> None:
    """Clowder yaml command private implementation"""

    if args.resolved:
        print(fmt.yaml_string(CLOWDER_CONTROLLER.get_yaml(resolved=True)))
    else:
        print_yaml()
