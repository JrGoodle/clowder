"""Clowder command line link controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand
from pygoodle.format import Format

import clowder.util.formatting as fmt
from clowder.controller import ClowderRepo, print_clowder_name, print_clowder_repo_status
from clowder.environment import clowder_repo_required, ENVIRONMENT
from clowder.util.error import ExistingSymlinkError
from clowder.util.yaml import link_clowder_yaml_default, link_clowder_yaml_version


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

        if args.version is None:
            link_clowder_yaml_default(ENVIRONMENT.clowder_dir)
        else:
            link_clowder_yaml_version(ENVIRONMENT.clowder_dir, args.version)
