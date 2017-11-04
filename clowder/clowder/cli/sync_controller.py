# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.clowder_repo import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.parallel import sync
from clowder.cli.util import options_help_message
from clowder.util.decorators import network_connection_required


class SyncController(ArgparseController):
    """Clowder sync command controller"""

    class Meta:
        """Clowder sync Meta configuration"""

        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Sync fork with upstream remote'

    @expose(
        help='this is the help message for clowder sync',
        arguments=[
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_fork_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_fork_project_names(),
                                                                  'projects to sync'))),
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

        all_fork_projects = CLOWDER_CONTROLLER.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        sync(CLOWDER_CONTROLLER, all_fork_projects, rebase=self.app.pargs.rebase, parallel=self.app.pargs.parallel)
