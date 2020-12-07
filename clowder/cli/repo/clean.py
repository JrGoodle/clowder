"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_git_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status


class RepoCleanCommand(Subcommand):

    name = 'clean'
    help = 'Discard changes in clowder repo'

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).clean()
