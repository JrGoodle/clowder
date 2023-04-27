"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import SingleArgument, Subcommand

from clowder.controller import (
    ClowderRepo,
    print_clowder_name,
    print_clowder_repo_status
)
from clowder.environment import clowder_git_repo_required, ENVIRONMENT


class RepoCommitCommand(Subcommand):
    class Meta:
        name = 'commit'
        help = 'Commit current changes in clowder repo'
        args = [
            SingleArgument('message', help='commit message')
        ]

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).commit(args.message[0])
