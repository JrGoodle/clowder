# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List, Optional

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message,
    validate_projects
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.util.parallel_commands import reset_parallel


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
            (['projects'], dict(metavar='PROJECT', default=['all'], nargs='+',
                                choices=CLOWDER_CONTROLLER.project_names,
                                help=options_help_message(CLOWDER_CONTROLLER.project_names,
                                                          'projects and groups to reset'))),
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--timestamp', '-t'], dict(choices=CLOWDER_CONTROLLER.project_names,
                                         default=None, nargs=1, metavar='TIMESTAMP',
                                         help='project to reset timestamps relative to'))
        ]
    )
    def reset(self) -> None:
        """Clowder reset command entry point"""

        self._reset()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _reset(self) -> None:
        """Clowder reset command private implementation"""

        timestamp_project = None
        if self.app.pargs.timestamp:
            timestamp_project = self.app.pargs.timestamp[0]
        reset(CLOWDER_CONTROLLER, self.app.pargs.projects, timestamp_project=timestamp_project,
              parallel=self.app.pargs.parallel)


def reset(clowder: ClowderController, project_names: List[str], timestamp_project: Optional[str] = None,
          parallel: bool = False) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD

    :param ClowderController clowder: ClowderController instance
    :param List[str] project_names: Project names to reset
    :param Optional[str] timestamp_project: Reference project to checkout other project commit timestamps relative to
    :param bool parallel: Whether command is being run in parallel, affects output
    """

    if parallel:
        reset_parallel(clowder, project_names, timestamp_project=timestamp_project)
        if os.name == "posix":
            return

    timestamp = None
    if timestamp_project:
        timestamp = clowder.get_timestamp(timestamp_project)

    projects = filter_projects(clowder.projects, project_names)
    validate_projects(projects)
    for project in projects:
        print(project.status())
        project.reset(timestamp=timestamp)
