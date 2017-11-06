# -*- coding: utf-8 -*-
"""Clowder command line start controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import (
    filter_groups,
    filter_projects_on_project_names,
    options_help_message,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.connectivity import network_connection_required


class StartController(ArgparseController):
    """Clowder start command controller"""

    class Meta:
        """Clowder start Meta configuration"""

        label = 'start'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Start a new branch'

    @expose(
        help='Start a new branch',
        arguments=[
            (['branch'], dict(help='name of branch to create', metavar='BRANCH')),
            (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to start'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to start'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
        ]
    )
    def start(self):
        """Clowder start command entry point"""

        self._start()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _start(self):
        """Clowder start command private implementation"""

        if self.app.pargs.tracking:
            self._start_tracking()
            return

        if self.app.pargs.projects is None:
            _start_groups(CLOWDER_CONTROLLER, self.app.pargs.groups, self.app.pargs.skip, self.app.pargs.branch)
        else:
            _start_projects(CLOWDER_CONTROLLER, self.app.pargs.projects, self.app.pargs.skip, self.app.pargs.branch)

    @network_connection_required
    def _start_tracking(self):
        """clowder start tracking command"""

        if self.app.pargs.projects is None:
            _start_groups(CLOWDER_CONTROLLER, self.app.pargs.groups, self.app.pargs.skip,
                          self.app.pargs.branch, tracking=True)
            return

        _start_projects(CLOWDER_CONTROLLER, self.app.pargs.projects, self.app.pargs.skip,
                        self.app.pargs.branch, tracking=True)


def _start_groups(clowder, group_names, skip, branch, tracking=False):
    """Start feature branch for groups

    .. py:function:: _start_groups(clowder, group_names, skip, branch, tracking=False)

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to create branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship
    """

    groups = filter_groups(clowder.groups, group_names)
    validate_groups(groups)
    for group in groups:
        run_group_command(group, skip, 'start', branch, tracking)


def _start_projects(clowder, project_names, skip, branch, tracking=False):
    """Start feature branch for projects

    .. py:function:: _start_projects(clowder, project_names, skip, branch, tracking=False)

    :param ClowderController clowder: ClowderController instance
    :param list[str] project_names: Project names to creat branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship
    """

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'start', branch, tracking)
