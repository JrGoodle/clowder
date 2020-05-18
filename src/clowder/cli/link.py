# -*- coding: utf-8 -*-
"""Clowder command line link controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from clowder import CLOWDER_DIR
from clowder.util.clowder_utils import (
    add_parser_arguments,
    get_saved_version_names,
    link_clowder_yaml,
    options_help_message
)
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status
)


def add_link_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    versions = get_saved_version_names()

    arguments = [
        (['version'], dict(metavar='VERSION', choices=versions, nargs='?', default=None,
                           help=options_help_message(versions, 'version to symlink')))
    ]

    parser = subparsers.add_parser('link', help='Symlink clowder.yaml version')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=link)


def link(args) -> None:
    """Clowder link command entry point"""

    _link(args)


@clowder_required
@print_clowder_repo_status
def _link(args) -> None:
    """Clowder link command private implementation"""

    link_clowder_yaml(CLOWDER_DIR, args.version)
