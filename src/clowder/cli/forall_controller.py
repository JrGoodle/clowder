# -*- coding: utf-8 -*-
"""Clowder command line forall controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List, Optional

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message,
    run_project_command
)
from clowder.util.decorators import valid_clowder_yaml_required
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
    def forall(self) -> None:
        """Clowder forall command entry point"""

        self._forall()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _forall(self) -> None:
        """Clowder forall command private implementation"""

        forall(CLOWDER_CONTROLLER, self.app.pargs.command, self.app.pargs.ignore_errors,
               group_names=self.app.pargs.groups, project_names=self.app.pargs.projects,
               skip=self.app.pargs.skip, parallel=self.app.pargs.parallel)


def forall(clowder: ClowderController, command: List[str], ignore_errors: bool,
           group_names: List[str], project_names: Optional[List[str]] = None,
           skip: Optional[List[str]] = None, parallel: bool = False) -> None:
    """Runs script in project directories specified

    .. py:function:: forall_script(clowder, command, ignore_errors, group_names, project_names=None, skip=[], parallel=False)

    :param ClowderController clowder: ClowderController instance
    :param list[str] command: Command or script and optional arguments
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    :param list[str] group_names: Group names to run command for
    :param Optional[List[str]] project_names: Project names to clean
    :param Optional[List[str]] skip: Project names to skip
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    skip = [] if skip is None else skip

    projects = filter_projects(clowder.groups, group_names=group_names, project_names=project_names)

    if parallel:
        forall_parallel([" ".join(command)], skip, ignore_errors, projects)
        if os.name == "posix":
            return

    for project in projects:
        run_project_command(project, skip, 'run', [" ".join(command)], ignore_errors)
