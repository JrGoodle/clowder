"""Clowder command line link controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse

from pygoodle.cli import add_parser_arguments

import clowder.util.formatting as fmt
from clowder.clowder_controller import print_clowder_name
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status
from clowder.environment import clowder_repo_required, ENVIRONMENT
from clowder.util.error import ExistingSymlinkError
from clowder.util.yaml import link_clowder_yaml_default, link_clowder_yaml_version


def add_link_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa
    """Add clowder link parser

    :param argparse._SubParsersAction subparsers: Subparsers action to add parser to
    """

    parser = subparsers.add_parser('link', help='Symlink clowder yaml version')
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.set_defaults(func=link)

    versions = ClowderRepo.get_saved_version_names()
    add_parser_arguments(parser, [
        (['version'], dict(metavar='<version>', choices=versions, nargs='?', default=None,
                           help=fmt.version_options_help_message('version to symlink', versions)))
    ])


@print_clowder_name
@clowder_repo_required
@print_clowder_repo_status
def link(args) -> None:
    """Clowder link command private implementation

    :raise ExistingSymlinkError:
    """

    if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
        raise ExistingSymlinkError(f"Found non-symlink file {fmt.path(ENVIRONMENT.clowder_yaml)} at target path")

    if args.version is None:
        link_clowder_yaml_default(ENVIRONMENT.clowder_dir)
    else:
        link_clowder_yaml_version(ENVIRONMENT.clowder_dir, args.version)
