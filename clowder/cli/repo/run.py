"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.app import SingleArgument, Subcommand

from clowder.controller import (
    ClowderRepo,
    print_clowder_name,
    print_clowder_repo_status
)
from clowder.environment import clowder_git_repo_required, ENVIRONMENT


class RepoRunCommand(Subcommand):
    class Meta:
        name = 'run'
        help = 'Run command in clowder repo'
        args = [
            SingleArgument('command', help='command to run in clowder repo directory')
        ]

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_repo_dir).run(args.command[0])
