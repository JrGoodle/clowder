# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.commands as commands
from clowder.cli import CLOWDER_CONTROLLER
from clowder.cli.util import project_names
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)


class ResetController(ArgparseController):
    class Meta:
        label = 'reset'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'
        project_names = project_names(CLOWDER_CONTROLLER)
        arguments = [
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--timestamp', '-t'], dict(choices=project_names, default=None, nargs=1, metavar='TIMESTAMP',
                                         help='project to reset timestamps relative to')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=project_names, nargs='+', metavar='PROJECT',
                                        help='projects to herd')),
            (['--skip', '-s'], dict(choices=project_names, nargs='+', metavar='PROJECT', default=[],
                                    help='projects to skip'))
            ]

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def default(self):
        timestamp_project = None
        if self.app.pargs.timestamp:
            timestamp_project = self.app.pargs.timestamp[0]
        commands.reset(CLOWDER_CONTROLLER, group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
                       skip=self.app.pargs.skip, timestamp_project=timestamp_project, parallel=self.app.pargs.parallel)
