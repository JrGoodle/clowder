# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.util.formatting as fmt
from clowder.cli import (
    CLOWDER_CONTROLLER,
    CLOWDER_REPO
)
from clowder.commands.util import run_group_command
from clowder.util.decorators import network_connection_required


class StatusController(ArgparseController):
    class Meta:
        label = 'status'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Print project status'
        arguments = [
            (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
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
