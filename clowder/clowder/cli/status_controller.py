# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import CLOWDER_REPO
from clowder.util.connectivity import network_connection_required
from clowder.util.clowder_utils import run_group_command


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
    def status(self):
        """Clowder status command entry point"""

        self._status()

    def _status(self):
        """Clowder status command private implementation"""

        if self.app.pargs.fetch:
            _fetch_projects(CLOWDER_REPO, CLOWDER_CONTROLLER)
        else:
            CLOWDER_REPO.print_status()

        padding = len(max(CLOWDER_CONTROLLER.get_all_project_paths(), key=len))

        for group in CLOWDER_CONTROLLER.groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                print(project.status(padding=padding))


@network_connection_required
def _fetch_projects(clowder_repo, clowder):
    """fetch all projects

    :param ClowderRepo clowder_repo: ClowderRepo instance
    :param ClowderController clowder: ClowderController instance
    """

    clowder_repo.print_status(fetch=True)

    print(' - Fetch upstream changes for projects\n')
    for group in clowder.groups:
        run_group_command(group, [], 'fetch_all')
