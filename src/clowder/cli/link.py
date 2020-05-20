# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder import CLOWDER_DIR
from clowder.util.clowder_utils import (
    add_parser_arguments,
    get_saved_version_names,
    link_clowder_yaml
)
from clowder.util.decorators import (
    print_clowder_name,
    clowder_repo_required,
    print_clowder_repo_status
)


def add_link_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    versions = get_saved_version_names()

    arguments = [
        (['version'], dict(metavar='VERSION', choices=versions, nargs='?', default=None,
                           help=fmt.options_help_message(versions, 'version to symlink')))
    ]

    parser = subparsers.add_parser('link', help='Symlink clowder.yaml version')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=link)


@clowder_repo_required
@print_clowder_name
@print_clowder_repo_status
def link(args) -> None:
    """Clowder link command private implementation"""

    link_clowder_yaml(CLOWDER_DIR, args.version)
