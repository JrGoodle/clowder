# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

import clowder.commands as commands
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import options_help_message
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)


class SyncController(ArgparseController):
    class Meta:
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
        self._sync()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _sync(self):
        all_fork_projects = CLOWDER_CONTROLLER.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        commands.sync(CLOWDER_CONTROLLER, all_fork_projects, rebase=self.app.pargs.rebase,
                      parallel=self.app.pargs.parallel)
