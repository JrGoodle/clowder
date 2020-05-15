# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import sync_parallel


class SyncController(ArgparseController):
    """Clowder sync command controller"""

    class Meta:
        """Clowder sync Meta configuration"""

        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Sync fork with upstream remote'

    @expose(
        help='Sync fork with upstream remote',
        arguments=[
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_fork_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_fork_project_names(),
                                                                  'projects to sync'))),
            (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel'))
        ]
    )
    def sync(self) -> None:
        """Clowder sync command entry point"""

        self._sync()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _sync(self) -> None:
        """Clowder sync command private implementation"""

        all_fork_projects = CLOWDER_CONTROLLER.get_all_fork_project_names()
        if not all_fork_projects:
            cprint(' - No forks to sync\n', 'red')
            return
        sync(CLOWDER_CONTROLLER, all_fork_projects,
             rebase=self.app.pargs.rebase,
             parallel=self.app.pargs.parallel)


def sync(clowder: ClowderController, project_names: List[str],
         rebase: bool = False, parallel: bool = False) -> None:
    """Sync projects

    :param ClowderController clowder: ClowderController instance
    :param list[str] project_names: Project names to sync
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    projects = filter_projects(clowder.projects, project_names)
    if parallel:
        sync_parallel(projects, rebase=rebase)
        if os.name == "posix":
            return

    for project in projects:
        project.sync(rebase=rebase)
