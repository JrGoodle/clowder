# -*- coding: utf-8 -*-
"""Clowder command line prune controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.error.clowder_error import ClowderError
from clowder.model.project import Project
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.clowder_utils import (
    existing_branch_projects,
    filter_projects,
    options_help_message,
    validate_projects
)


class PruneController(ArgparseController):
    """Clowder prune command controller"""

    class Meta:
        """Clowder prune Meta configuration"""

        label = 'prune'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Prune branches'

    @expose(
        help='Prune branches',
        arguments=[
            (['branch'], dict(help='name of branch to remove', metavar='BRANCH')),
            (['--force', '-f'], dict(action='store_true', help='force prune branches')),
            (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='prune remote branches')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to prune')))
        ]
    )
    def prune(self) -> None:
        """Clowder prune command entry point"""

        self._prune()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _prune(self) -> None:
        """Clowder prune command private implementation"""

        if self.app.pargs.all:
            self._prune_all()
            return

        if self.app.pargs.remote:
            self._prune_remote()
            return

        _prune(CLOWDER_CONTROLLER, self.app.pargs.projects, self.app.pargs.branch,
               force=self.app.pargs.force, local=True)

    @network_connection_required
    def _prune_all(self) -> None:
        """clowder prune all command"""

        _prune(CLOWDER_CONTROLLER, self.app.pargs.projects, self.app.pargs.branch,
               force=self.app.pargs.force, local=True, remote=True)

    @network_connection_required
    def _prune_remote(self) -> None:
        """clowder prune remote command"""

        _prune(CLOWDER_CONTROLLER, self.app.pargs.projects, self.app.pargs.branch, remote=True)


def _prune(clowder: ClowderController, project_names: List[str], branch: str, force: bool = False,
           local: bool = False, remote: bool = False) -> None:
    """Prune branches

    :param ClowderController clowder: ClowderController instance
    :param List[str] project_names: Project names to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    """

    projects = filter_projects(clowder.projects, project_names)
    validate_projects(projects)
    _prune_projects(projects, branch, force=force, local=local, remote=remote)


def _prune_projects(projects: List[Project], branch: str, force: bool = False, local: bool = False,
                    remote: bool = False) -> None:
    """Prune project branches

    :param list[Project] projects: Projects to prune
    :param str branch: Branch to prune
    :param bool force: Force delete branch
    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    """

    local_branch_exists = existing_branch_projects(projects, branch, is_remote=False)
    remote_branch_exists = existing_branch_projects(projects, branch, is_remote=True)

    try:
        _validate_branches(local, remote, local_branch_exists, remote_branch_exists)
    except ClowderError:
        pass
    else:
        for project in projects:
            print(project.status())
            project.prune(branch, force=force, local=local, remote=remote)


def _validate_branches(local: bool, remote: bool, local_branch_exists: bool, remote_branch_exists: bool) -> None:
    """Prune project branches

    :param bool local: Delete local branch
    :param bool remote: Delete remote branch
    :param bool local_branch_exists: Whether a local branch exists
    :param bool remote_branch_exists: Whether a remote branch exists
    :raise ClowderError:
    """

    if local and remote:
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune local and remote branches\n')
        return

    if remote:
        if not remote_branch_exists:
            cprint(' - No remote branches to prune\n', 'red')
            raise ClowderError
        print(' - Prune remote branches\n')
        return

    if not local_branch_exists:
        print(' - No local branches to prune\n')
        raise ClowderError
    print(' - Prune local branches\n')
