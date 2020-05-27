# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder import CLOWDER_DIR
from clowder.clowder_repo import get_saved_version_names
from clowder.util.yaml import (
    link_clowder_yaml_default,
    link_clowder_yaml_version
)
from clowder.util.decorators import (
    print_clowder_name,
    clowder_repo_required,
    print_clowder_repo_status
)

from .util import add_parser_arguments


def add_link_parser(subparsers: argparse._SubParsersAction) -> None: # noqa
    """Add clowder link parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    versions = get_saved_version_names()

    arguments = [
        (['version'], dict(metavar='VERSION', choices=versions, nargs='?', default=None,
                           help=fmt.options_help_message(versions, 'version to symlink')))
    ]

    parser = subparsers.add_parser('link', help='Symlink clowder yaml version')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=link)


@clowder_repo_required
@print_clowder_name
@print_clowder_repo_status
def link(args) -> None:
    """Clowder link command private implementation"""

    if args.version is None:
        link_clowder_yaml_default(CLOWDER_DIR)
    else:
        link_clowder_yaml_version(CLOWDER_DIR, args.version)
