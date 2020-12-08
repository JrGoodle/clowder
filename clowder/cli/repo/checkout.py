"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import SingleArgument, Subcommand

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_git_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status_fetch


class RepoCheckoutCommand(Subcommand):
    class Meta:
        name = 'checkout'
        help = 'Checkout ref in clowder repo'
        args = [
            SingleArgument('ref', help='git ref to checkout')
        ]

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status_fetch
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).checkout(args.ref[0])
