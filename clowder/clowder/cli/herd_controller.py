# -*- coding: utf-8 -*-
"""Clowder command line herd controller

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
            (['--protocol'], dict(choices=['https', 'ssh'], nargs=1, default=None, metavar='PROTOCOL',
                                  help='Protocol to clone new repos with')),
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
    def herd(self):
        """Clowder herd command entry point"""

        self._herd()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _herd(self):
        """Clowder herd command private implementation"""

        branch = None if self.app.pargs.branch is None else self.app.pargs.branch[0]
        tag = None if self.app.pargs.tag is None else self.app.pargs.tag[0]
        depth = None if self.app.pargs.depth is None else self.app.pargs.depth[0]
        protocol = None if self.app.pargs.protocol is None else self.app.pargs.protocol[0]

        kwargs = {'group_names': self.app.pargs.groups, 'project_names': self.app.pargs.projects,
                  'skip': self.app.pargs.skip, 'branch': branch, 'tag': tag,
                  'depth': depth, 'rebase': self.app.pargs.rebase, 'protocol': protocol}

        if self.app.pargs.parallel:
            herd_parallel(CLOWDER_CONTROLLER, **kwargs)
            if os.name == "posix":
                return

        herd(CLOWDER_CONTROLLER, **kwargs)


def herd(clowder, group_names, **kwargs):
    """Clone projects or update latest from upstream

    .. py:function:: herd(clowder, group_names, branch=None, tag=None, depth=0, rebase=False, project_names=None, skip=[], protocol=None)

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to herd

    Keyword Args:
        branch (str): Branch to attempt to herd
        tag (str): Tag to attempt to herd
        depth (int): Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        protocol (str): Git protocol ('ssh' or 'https')
        rebase (bool): Whether to use rebase instead of pulling latest changes
        project_names (list[str]) project_names: Project names to herd
        skip (list[str]): Project names to skip
    """

    project_names = kwargs.get('project_names', None)
    skip = kwargs.get('skip', [])
    branch = kwargs.get('branch', None)
    tag = kwargs.get('tag', None)
    depth = kwargs.get('depth', None)
    rebase = kwargs.get('rebase', False)
    protocol = kwargs.get('protocol', None)

    if project_names is None:
        groups = filter_groups(clowder.groups, group_names)
        validate_groups(groups)
        for group in groups:
            run_group_command(group, skip, 'herd', branch=branch, tag=tag,
                              depth=depth, rebase=rebase, protocol=protocol)
        return

    projects = filter_projects(clowder.groups, project_names=project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'herd', branch=branch, tag=tag,
                            depth=depth, rebase=rebase, protocol=protocol)
