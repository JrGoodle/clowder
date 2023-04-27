"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Subcommand

from clowder.controller import (
    ClowderRepo,
    print_clowder_name,
    print_clowder_repo_status
)
from clowder.environment import clowder_git_repo_required, ENVIRONMENT


class RepoCleanCommand(Subcommand):
    class Meta:
        name = 'clean'
        help = 'Discard changes in clowder repo'

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).repo.clean()
