# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER, ClowderController
from clowder.clowder_repo import CLOWDER_REPO, ClowderRepo
from clowder.util.connectivity import network_connection_required
from clowder.util.decorators import valid_clowder_yaml_required


class StatusController(ArgparseController):
    """Clowder status command controller"""

    class Meta:
        """Clowder status Meta configuration"""

        label = 'status'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Print project status'

    @expose(
        help='Print project status',
        arguments=[
            (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
        ]
    )
    def status(self) -> None:
        """Clowder status command entry point"""

        self._status()

    @valid_clowder_yaml_required
    def _status(self) -> None:
        """Clowder status command private implementation"""

        if self.app.pargs.fetch:
            _fetch_projects(CLOWDER_REPO, CLOWDER_CONTROLLER)
        else:
            CLOWDER_REPO.print_status()

        padding = len(max(CLOWDER_CONTROLLER.get_all_project_paths(), key=len))

        for project in CLOWDER_CONTROLLER.projects:
            print(project.status(padding=padding))


@network_connection_required
def _fetch_projects(clowder_repo: ClowderRepo, clowder: ClowderController) -> None:
    """fetch all projects

    :param ClowderRepo clowder_repo: ClowderRepo instance
    :param ClowderController clowder: ClowderController instance
    """

    clowder_repo.print_status(fetch=True)

    print(' - Fetch upstream changes for projects\n')
    for project in clowder.projects:
        print(project.status())
        project.fetch_all()
