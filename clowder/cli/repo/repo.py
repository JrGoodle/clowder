"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand

from .add import RepoAddCommand
from .checkout import RepoCheckoutCommand
from .clean import RepoCleanCommand
from .commit import RepoCommitCommand
from .pull import RepoPullCommand
from .push import RepoPushCommand
from .run import RepoRunCommand
from .status import RepoStatusCommand


class RepoCommand(Subcommand):
    class Meta:
        name = 'repo'
        help = 'Manage clowder repo'
        subcommands = [
            RepoAddCommand,
            RepoCheckoutCommand,
            RepoCleanCommand,
            RepoCommitCommand,
            RepoPullCommand,
            RepoPushCommand,
            RepoRunCommand,
            RepoStatusCommand
        ]

    def run(self, args) -> None:
        self.print_help()
