# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.commands as commands
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


class ForallController(ArgparseController):
    class Meta:
        label = 'forall'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Run command or script in project directories'

    @expose(
        help='this is the help message for clowder forall',
        arguments=[
            (['--command', '-c'], dict(nargs=1, metavar='COMMAND',
                                       help='command or script to run in project directories')),
            (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT', help='projects to herd')),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[], help='projects to skip'))
            ]
    )
    def forall(self):
        self._forall()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _forall(self):
        commands.forall(CLOWDER_CONTROLLER, self.app.pargs.command[0], self.app.pargs.ignore_errors,
                        group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
                        skip=self.app.pargs.skip, parallel=self.app.pargs.parallel)
