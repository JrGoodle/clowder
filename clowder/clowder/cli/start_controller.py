# -*- coding: utf-8 -*-
"""Clowder command line start controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_repo import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)
from clowder.util.decorators import network_connection_required


class StartController(ArgparseController):
    """Clowder start command controller"""

    class Meta:
        """Clowder start Meta configuration"""

        label = 'start'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Start a new branch'

    @expose(
        help='this is the help message for clowder start',
        arguments=[
            (['branch'], dict(help='name of branch to create', metavar='BRANCH')),
            (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT', help='projects to herd')),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[], help='projects to skip'))
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

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to create branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    groups = filter_groups(clowder.groups, group_names)
    validate_groups(groups)
    for group in groups:
        run_group_command(group, skip, 'start', branch, tracking)


def _start_projects(clowder, project_names, skip, branch, tracking=False):
    """Start feature branch for projects

    :param ClowderController clowder: ClowderController instance
    :param list[str] project_names: Project names to creat branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'start', branch, tracking)
