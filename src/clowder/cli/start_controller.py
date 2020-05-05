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
    filter_projects,
    options_help_message,
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
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to start')))
        ]
    )
    def start(self) -> None:
        """Clowder start command entry point"""

        self._start()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _start(self) -> None:
        """Clowder start command private implementation"""

        if self.app.pargs.tracking:
            self._start_tracking()
            return

        self._start_branches(False)

    @network_connection_required
    def _start_tracking(self) -> None:
        """clowder start tracking command"""

        self._start_branches(True)

    def _start_branches(self, tracking: bool) -> None:
        """clowder start branches command

        :param bool tracking: Whether to create tracking branches
        """

        projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
        validate_projects(projects)
        for project in projects:
            print(project.status())
            project.start(self.app.pargs.branch, tracking)
