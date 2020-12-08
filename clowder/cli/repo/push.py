"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand
from pygoodle.connectivity import network_connection_required

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_git_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status_fetch


class RepoPushCommand(Subcommand):
    class Meta:
        name = 'push'
        help = 'Push changes in clowder repo'

    @print_clowder_name
    @clowder_git_repo_required
    @network_connection_required
    @print_clowder_repo_status_fetch
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).push()
