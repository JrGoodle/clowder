"""Clowder command line prune controller

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Tuple

from pygoodle.app import Argument, BoolArgument, MutuallyExclusiveArgumentGroup, Subcommand
from pygoodle.connectivity import network_connection_required
from pygoodle.console import CONSOLE

from clowder.clowder_controller import CLOWDER_CONTROLLER, print_clowder_name, valid_clowder_yaml_required
from clowder.config import Config
from clowder.git import ProjectRepo
from clowder.git.clowder_repo import print_clowder_repo_status
from clowder.util.error import CommandArgumentError

from .util import ProjectsArgument


class PruneCommand(Subcommand):
    class Meta:
        name = 'prune'
        help = 'Prune branches'
        args = [
            Argument('branch', help='name of branch to remove'),
            ProjectsArgument('projects and groups to prune'),
            BoolArgument('--force', '-f', help='force prune branches')
        ]
        mutually_exclusive_args = [
            MutuallyExclusiveArgumentGroup(
                args=[
                    BoolArgument('--all', '-a', help='prune local and remote branches'),
                    BoolArgument('--remote', '-r', help='prune remote branches')
                ]
            )
        ]

    @valid_clowder_yaml_required
    @print_clowder_name
    @print_clowder_repo_status
    def run(self, args) -> None:
        if args.all:
            self._prune_all(args)
            return

        if args.remote:
            self._prune_remote(args)
            return

        self._prune_impl(args.projects, args.branch, force=args.force, local=True)

    @network_connection_required
    def _prune_all(self, args) -> None:
        """clowder prune all command"""

        self._prune_impl(args.projects, args.branch, force=args.force, local=True, remote=True)

    @network_connection_required
    def _prune_remote(self, args) -> None:
        """clowder prune remote command"""

        self._prune_impl(args.projects, args.branch, remote=True)

    def _prune_impl(self, project_names: List[str], branch: str, force: bool = False,
                    local: bool = False, remote: bool = False) -> None:
        """Prune branches

        :param List[str] project_names: Project names to prune
        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        """

        projects = Config().process_projects_arg(project_names)
        projects = CLOWDER_CONTROLLER.filter_projects(CLOWDER_CONTROLLER.projects, projects)

        CLOWDER_CONTROLLER.validate_projects_state(projects)
        self._prune_projects(projects, branch, force=force, local=local, remote=remote)

    @staticmethod
    def _prune_projects(projects: Tuple[ProjectRepo, ...], branch: str, force: bool = False,
                        local: bool = False, remote: bool = False) -> None:
        """Prune project branches

        :param Tuple[Project, ...] projects: Projects to prune
        :param str branch: Branch to prune
        :param bool force: Force delete branch
        :param bool local: Delete local branch
        :param bool remote: Delete remote branch
        :raise CommandArgumentError:
        """

        local_branch_exists = CLOWDER_CONTROLLER.project_has_local_branch(projects, branch)
        remote_branch_exists = CLOWDER_CONTROLLER.project_has_remote_branch(projects, branch)

        if local and remote:
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                CONSOLE.stdout(' - No local or remote branches to prune')
                return
            CONSOLE.stdout(' - Prune local and remote branches\n')
        elif remote:
            if not remote_branch_exists:
                CONSOLE.stdout(' - No remote branches to prune')
                return
            CONSOLE.stdout(' - Prune remote branches\n')
        elif local:
            if not local_branch_exists:
                CONSOLE.stdout(' - No local branches to prune')
                return
            CONSOLE.stdout(' - Prune local branches\n')
        else:
            raise CommandArgumentError('local and remote are both false, but at least one should be true')

        for project in projects:
            CONSOLE.stdout(project.status())
            project.prune(branch, force=force, local=local, remote=remote)
