# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from cement.ext.ext_argparse import expose

import clowder.commands as commands
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.cli.util import project_names
from clowder.clowder_controller import ClowderController
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)


class ResetController(AbstractBaseController):
    class Meta:
        label = 'reset'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'

        clowder = None
        try:
            clowder = ClowderController(os.getcwd())
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except:
            pass
        finally:
            project_names = project_names(clowder)
            arguments = AbstractBaseController.Meta.arguments + [
                (['--parallel'], dict(action='store_true', help='run commands in parallel')),
                (['--timestamp', '-t'], dict(choices=project_names, default=None, nargs=1, metavar='TIMESTAMP',
                                             help='project to reset timestamps relative to'))
                ]

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def default(self):
        timestamp_project = None
        if self.app.pargs.timestamp:
            timestamp_project = self.app.pargs.timestamp[0]
        commands.reset(self.clowder, group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
                       skip=self.app.pargs.skip, timestamp_project=timestamp_project, parallel=self.app.pargs.parallel)
