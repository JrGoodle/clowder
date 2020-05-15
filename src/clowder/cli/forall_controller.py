# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import forall_parallel


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
            (['projects'], dict(metavar='PROJECT', default=['all'], nargs='+',
                                choices=CLOWDER_CONTROLLER.project_names,
                                help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                          'projects and groups to run command for'))),
            (['--command', '-c'], dict(nargs='+', metavar='COMMAND', default=None,
                                       help='command or script to run in project directories')),
            (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel'))
        ]
    )
    def forall(self) -> None:
        """Clowder forall command entry point"""

        self._forall()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _forall(self) -> None:
        """Clowder forall command private implementation"""

        forall(CLOWDER_CONTROLLER, self.app.pargs.command, self.app.pargs.ignore_errors,
               project_names=self.app.pargs.projects, parallel=self.app.pargs.parallel)


def forall(clowder: ClowderController, command: List[str], ignore_errors: bool,
           project_names: List[str], parallel: bool = False) -> None:
    """Runs script in project directories specified

    :param ClowderController clowder: ClowderController instance
    :param list[str] command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param List[str] project_names: Project names to clean
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    projects = filter_projects(clowder.projects, project_names)

    if parallel:
        forall_parallel([" ".join(command)], projects, ignore_errors)
        if os.name == "posix":
            return

    for project in projects:
        print(project.status())
        project.run([" ".join(command)], ignore_errors)
