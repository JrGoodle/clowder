"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status


class RepoStatusCommand(Subcommand):

    name = 'status'
    help = 'Print clowder repo git status'
    args = [
        Argument('files', nargs='+', help='files to add')
    ]

    @print_clowder_name
    @clowder_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        if ENVIRONMENT.clowder_git_repo_dir is not None:
            ClowderRepo(ENVIRONMENT.clowder_repo_dir).git_status()
