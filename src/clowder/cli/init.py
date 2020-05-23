# -*- coding: utf-8 -*-
"""Clowder command line init controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import os

from termcolor import colored, cprint

import clowder.clowder_repo as clowder_repo
from clowder import CURRENT_DIR
from clowder.error import ClowderExit
from clowder.git.util import existing_git_repository
from clowder.util.clowder_utils import add_parser_arguments
from clowder.util.connectivity import network_connection_required


def add_init_parser(subparsers: argparse._SubParsersAction) -> None: # noqa

    arguments = [
        (['url'], dict(metavar='URL', help='url of repo containing clowder.yaml')),
        (['--branch', '-b'], dict(nargs=1, metavar='BRANCH', help='branch of repo containing clowder.yaml'))
    ]

    parser = subparsers.add_parser('init', help='Clone repository to clowder directory and create clowder.yaml symlink')
    add_parser_arguments(parser, arguments)
    parser.set_defaults(func=init)


@network_connection_required
def init(args) -> None:
    """Clowder init command private implementation

    :raise ClowderExit:
    """

    clowder_repo_dir = os.path.join(CURRENT_DIR, '.clowder')
    if existing_git_repository(clowder_repo_dir):
        cprint('Clowder already initialized in this directory\n', 'red')
        raise ClowderExit(1)

    url_output = colored(args.url, 'green')
    print(f"Create clowder repo from {url_output}\n")
    if args.branch is None:
        branch = 'master'
    else:
        branch = str(args.branch[0])
    clowder_repo.init(args.url, branch)
