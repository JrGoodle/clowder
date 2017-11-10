# -*- coding: utf-8 -*-
"""Clowder command line start controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    filter_groups,
    filter_projects,
    options_help_message,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)


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

        self._start_branches(False)

    @network_connection_required
    def _start_tracking(self):
        """clowder start tracking command"""

        self._start_branches(True)

    def _start_branches(self, tracking):
        """clowder start branches command"""

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            validate_groups(groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'start', self.app.pargs.branch, tracking)
            return

        projects = filter_projects(CLOWDER_CONTROLLER.groups, project_names=self.app.pargs.projects)
        validate_projects(projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'start', self.app.pargs.branch, tracking)
