"""Clowder command line init controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo
from clowder.util.console import CONSOLE
from clowder.util.logging import LOG
from clowder.util.connectivity import network_connection_required

from .util import add_parser_arguments


def add_init_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa

    parser = subparsers.add_parser('init', help='Clone repository to clowder directory and create clowder yaml symlink')
    parser.set_defaults(func=init)

    add_parser_arguments(parser, [
        (['url'], dict(metavar='<url>', help='url of repo containing clowder yaml file')),
        (['--branch', '-b'], dict(nargs=1, metavar='<branch>', help='branch of repo containing clowder yaml file'))
    ])


@network_connection_required
def init(args) -> None:
    """Clowder init command private implementation"""

    clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
    if clowder_repo_dir.is_dir():
        try:
            clowder_repo_dir.rmdir()
        except OSError:
            LOG.error("Clowder already initialized in this directory")
            raise

    CONSOLE.stdout(f"Create clowder repo from {fmt.green(args.url)}\n")
    if args.branch is None:
        branch = 'master'
    else:
        branch = str(args.branch[0])
    clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
    repo = ClowderRepo(clowder_repo_dir)
    repo.init(args.url, branch)
