# -*- coding: utf-8 -*-
"""Clowder command line herd controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import List, Optional

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
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
from clowder.util.parallel_commands import herd_parallel


class HerdController(ArgparseController):
    """Clowder herd command controller"""

    class Meta:
        """Clowder herd Meta configuration"""

        label = 'herd'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Clone and update projects with latest changes'

    @expose(
        help='Clone and update projects with latest changes',
        arguments=[
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
            (['--depth', '-d'], dict(default=None, type=int, nargs=1, metavar='DEPTH', help='depth to herd')),
            (['--branch', '-b'], dict(nargs=1, default=None, metavar='BRANCH', help='branch to herd if present')),
            (['--tag', '-t'], dict(nargs=1, default=None, metavar='TAG', help='tag to herd if present')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to herd'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to herd'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
            ]
    )
    def herd(self) -> None:
        """Clowder herd command entry point"""

        self._herd()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _herd(self) -> None:
        """Clowder herd command private implementation"""

        branch = None if self.app.pargs.branch is None else self.app.pargs.branch[0]
        tag = None if self.app.pargs.tag is None else self.app.pargs.tag[0]
        depth = None if self.app.pargs.depth is None else self.app.pargs.depth[0]
        group_names = self.app.pargs.groups
        project_names = self.app.pargs.projects
        skip = self.app.pargs.skip
        rebase = self.app.pargs.rebase

        if self.app.pargs.parallel:
            herd_parallel(CLOWDER_CONTROLLER, branch=branch, tag=tag, depth=depth,
                          group_names=group_names, project_names=project_names, skip=skip, rebase=rebase)
            if os.name == "posix":
                return

        herd(CLOWDER_CONTROLLER, branch=branch, tag=tag, depth=depth,
             group_names=group_names, project_names=project_names, skip=skip, rebase=rebase)


def herd(clowder: ClowderController, group_names: List[str], branch: Optional[str] = None,
         tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False,
         project_names: Optional[List[str]] = None, skip: Optional[List[str]] = None) -> None:
    """Clone projects or update latest from upstream

    .. py:function:: herd(clowder, group_names, branch=None, tag=None, depth=0, rebase=False, project_names=None, skip=[])

    :param ClowderController clowder: ClowderController instance
    :param List[str] group_names: Group names to herd
    :param Optional[str] branch: Branch to attempt to herd
    :param Optional[str] tag: Tag to attempt to herd
    :param Optonal[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    :param Optional[List[str]] project_names: Project names to herd
    :param Optional[List[str]] skip: Project names to skip
    """

    skip = [] if skip is None else skip

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        validate_groups(groups)
        for group in groups:
            run_group_command(group, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
