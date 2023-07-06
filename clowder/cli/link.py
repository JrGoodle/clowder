"""Clowder command line link controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import Argument, Subcommand
from clowder.util.format import Format

import clowder.util.formatting as fmt
from clowder.controller import ClowderRepo, print_clowder_name, print_clowder_repo_status
from clowder.environment import clowder_repo_required, ENVIRONMENT
from clowder.util.error import ExistingSymlinkError
from clowder.util.yaml import link_clowder_yaml


class LinkCommand(Subcommand):
    class Meta:
        name = 'link'
        help = 'Symlink clowder yaml version'
        versions = ClowderRepo.saved_version_names()
        args = [
            Argument('version', choices=versions, nargs='?', default=None,
                     help=fmt.version_options_help_message('version to symlink', versions))
        ]

    @print_clowder_name
    @clowder_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        if ENVIRONMENT.clowder_yaml is not None and not ENVIRONMENT.clowder_yaml.is_symlink():
            raise ExistingSymlinkError(f"Found non-symlink file {Format.path(ENVIRONMENT.clowder_yaml)} at target path")
        link_clowder_yaml(ENVIRONMENT.clowder_dir, version=args.version)
