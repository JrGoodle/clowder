# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status_fetch
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required
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
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_fork_project_names(),
                                                                  'projects to sync'))),
            (['--protocol'], dict(choices=['https', 'ssh'], nargs=1, default=None, metavar='PROTOCOL',
                                  help='Protocol to clone new repos with')),
            (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel'))
        ]
    )
    def sync(self):
        """Clowder sync command entry point"""

        self._sync()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _sync(self):
        """Clowder sync command private implementation"""

        protocol = None if self.app.pargs.protocol is None else self.app.pargs.protocol[0]

        all_fork_projects = CLOWDER_CONTROLLER.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            return
        sync(CLOWDER_CONTROLLER, all_fork_projects, protocol=protocol,
             rebase=self.app.pargs.rebase,
             parallel=self.app.pargs.parallel)


def sync(clowder, project_names, protocol, rebase=False, parallel=False):
    """Sync projects

    .. py:function:: sync(clowder, project_names, protocol, rebase=False, parallel=False)

    :param ClowderController clowder: ClowderController instance
    :param list[str] project_names: Project names to sync
    :param str protocol: Git protocol, 'ssh' or 'https'
    :param Optional[bool] rebase: Whether to use rebase instead of pulling latest changes
    :param Optional[bool] parallel: Whether command is being run in parallel, affects output
    """

    projects = filter_projects(clowder.groups, project_names=project_names)
    if parallel:
        sync_parallel(projects, protocol, rebase=rebase)
        if os.name == "posix":
            return

    for project in projects:
        project.sync(protocol, rebase=rebase)
