# -*- coding: utf-8 -*-
"""Clowder command line reset controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status_fetch
from clowder.util.clowder_utils import (
    filter_groups,
    filter_projects,
    options_help_message,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required
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
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--timestamp', '-t'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
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


def reset(clowder, group_names, **kwargs):
    """Reset project branches to upstream or checkout tag/sha as detached HEAD

    .. py:function:: reset(clowder, group_names, timestamp_project=None, parallel=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to reset

    Keyword Args:
        timestamp_project (str): Reference project to checkout commit timestamps of other projects relative to
        parallel (bool): Whether command is being run in parallel, affects output
        project_names (list[str]): Project names to reset
        skip (list[str]): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    timestamp_project = kwargs.get('timestamp_project', None)
    parallel = kwargs.get('parallel', False)

    if parallel:
        reset_parallel(clowder, group_names, skip=skip, timestamp_project=timestamp_project)
        if os.name == "posix":
            return

    timestamp = None
    if timestamp_project:
        timestamp = clowder.get_timestamp(timestamp_project)
    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        validate_groups(groups)
        for group in groups:
            run_group_command(group, skip, 'reset', timestamp=timestamp)
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'reset', timestamp=timestamp)
