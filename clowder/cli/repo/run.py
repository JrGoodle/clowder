"""Clowder command line repo controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, Subcommand

from clowder.clowder_controller import print_clowder_name
from clowder.environment import clowder_git_repo_required, ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo, print_clowder_repo_status


class RepoRunCommand(Subcommand):
    class Meta:
        name = 'run'
        help = 'Run command in clowder repo'
        args = [
            Argument('command', nargs=1, help='command to run in clowder repo directory')
        ]

    @print_clowder_name
    @clowder_git_repo_required
    @print_clowder_repo_status
    def run(self, args) -> None:
        ClowderRepo(ENVIRONMENT.clowder_repo_dir).run_command(args.command[0])
