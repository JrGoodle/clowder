# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.parallel import reset
from clowder.clowder_repo import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import (
    options_help_message,
    project_names
)
from clowder.util.connectivity import network_connection_required


class ResetController(ArgparseController):
    """Clowder reset command controller"""

    class Meta:
        """Clowder reset Meta configuration"""

        label = 'reset'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'

    @expose(
        help='Reset branches to upstream commits or check out detached HEADs for tags and shas',
        arguments=[
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--timestamp', '-t'], dict(choices=project_names(CLOWDER_CONTROLLER),
                                         default=None, nargs=1, metavar='TIMESTAMP',
                                         help='project to reset timestamps relative to')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to reset'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to reset'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
            ]
    )
    def reset(self):
        """Clowder reset command entry point"""

        self._reset()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _reset(self):
        """Clowder reset command private implementation"""

        timestamp_project = None
        if self.app.pargs.timestamp:
            timestamp_project = self.app.pargs.timestamp[0]
        reset(CLOWDER_CONTROLLER, group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
              skip=self.app.pargs.skip, timestamp_project=timestamp_project, parallel=self.app.pargs.parallel)
