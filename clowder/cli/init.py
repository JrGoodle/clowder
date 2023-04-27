"""Clowder command line init controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import Argument, SingleArgument, Subcommand
from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE
from pygoodle.format import Format

from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.controller import ClowderRepo


class InitCommand(Subcommand):
    class Meta:
        name = 'init'
        help = 'Clone repository to clowder directory and create clowder yaml symlink'
        args = [
            Argument('url', help='url of repo containing clowder yaml file'),
            SingleArgument('--branch', '-b', help='branch of repo containing clowder yaml file')
        ]

    @network_connection_required
    def run(self, args) -> None:
        clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
        if clowder_repo_dir.is_dir():
            try:
                clowder_repo_dir.rmdir()
            except OSError:
                LOG.error("Clowder already initialized in this directory")
                raise

        CONSOLE.stdout(f"Create clowder repo from {Format.green(args.url)}\n")
        branch = None if args.branch is None else str(args.branch[0])
        clowder_repo_dir = ENVIRONMENT.current_dir / '.clowder'
        repo = ClowderRepo(clowder_repo_dir)
        repo.init(args.url, branch=branch)
