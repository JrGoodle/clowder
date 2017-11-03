# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from cement.ext.ext_argparse import expose
from termcolor import cprint

import clowder.commands as commands
from clowder.clowder_controller import ClowderController
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.cli.util import (
    fork_project_names,
    options_help_message
)
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)


class SyncController(AbstractBaseController):
    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Sync fork with upstream remote'
        clowder = None
        try:
            clowder = ClowderController(os.getcwd())
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except:
            pass
        finally:
            project_names = fork_project_names(clowder)
            projects_help = options_help_message(project_names, 'projects to sync')
            arguments = [
                (['--projects', '-p'], dict(choices=project_names, nargs='+', metavar='PROJECT', help=projects_help)),
                (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
                (['--parallel'], dict(action='store_true', help='run commands in parallel'))
                ]

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def default(self):
        all_fork_projects = self.clowder.get_all_fork_project_names()
        if all_fork_projects == '':
            cprint(' - No forks to sync\n', 'red')
            sys.exit()
        commands.sync(self.clowder, all_fork_projects, rebase=self.app.pargs.rebase, parallel=self.app.pargs.parallel)
