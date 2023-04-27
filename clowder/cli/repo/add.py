"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand

from clowder.controller import (
    ClowderRepo,
    print_clowder_name,
    print_clowder_repo_status
)
from clowder.environment import clowder_git_repo_required, ENVIRONMENT


class RepoAddCommand(Subcommand):
    class Meta:
        name = 'add'
        help = 'Add files in clowder repo'
        args = [
            Argument('files', nargs='+', help='files to add')
        ]

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).add_files(args.files)
