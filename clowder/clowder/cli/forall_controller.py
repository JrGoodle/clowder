# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.parallel import forall
from clowder.cli.util import options_help_message
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required


class ForallController(ArgparseController):
    """Clowder forall command controller"""

    class Meta:
        """Clowder forall Meta configuration"""

        label = 'forall'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Run command or script in project directories'

    @expose(
        help='Run command or script in project directories',
        arguments=[
            (['--command', '-c'], dict(nargs='+', metavar='COMMAND', default=None,
                                       help='command or script to run in project directories')),
            (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to run command for'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to run command for'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
            ]
    )
    def forall(self):
        """Clowder forall command entry point"""

        self._forall()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _forall(self):
        """Clowder forall command private implementation"""

        forall(CLOWDER_CONTROLLER, self.app.pargs.command, self.app.pargs.ignore_errors,
               group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
               skip=self.app.pargs.skip, parallel=self.app.pargs.parallel)
