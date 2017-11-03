# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import expose

import clowder.commands as commands
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


class ForallController(AbstractBaseController):
    class Meta:
        label = 'forall'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run command or script in project directories'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--command', '-c'], dict(nargs=1, metavar='COMMAND',
                                       help='command or script to run in project directories')),
            (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel'))
            ]

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        commands.forall(self.clowder, self.app.pargs.command[0], self.app.pargs.ignore_errors,
                        group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
                        skip=self.app.pargs.skip, parallel=self.app.pargs.parallel)
