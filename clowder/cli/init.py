# -*- coding: utf-8 -*-
"""Clowder command line init controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from termcolor import colored

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import network_connection_required

from .util import add_parser_arguments


def add_init_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['url'], dict(metavar='<url>', help='url of repo containing clowder yaml file')),
        (['--branch', '-b'], dict(nargs=1, metavar='<branch>', help='branch of repo containing clowder yaml file'))
    ]

    parser = subparsers.add_parser('init', help='Clone repository to clowder directory and create clowder yaml symlink')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=init)


@network_connection_required
def init(args) -> None:
    """Clowder init command private implementation

    :raise ClowderError:
    """

    clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
    if clowder_repo_dir.is_dir():
        try:
            clowder_repo_dir.rmdir()
        except OSError as err:
            LOG_DEBUG('Failed to remove existing .clowder directory', err)
            raise ClowderError(ClowderErrorType.CLOWDER_ALREADY_INITIALIZED, fmt.error_clowder_already_initialized())

    url_output = colored(args.url, 'green')
    print(f"Create clowder repo from {url_output}\n")
    if args.branch is None:
        branch = 'master'
    else:
        branch = str(args.branch[0])
    clowder_repo.init(args.url, branch)
