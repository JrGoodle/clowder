# -*- coding: utf-8 -*-
"""Clowder command line status controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import expose

import clowder.util.formatting as fmt
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.commands.util import run_group_command
from clowder.util.decorators import network_connection_required


class StatusController(AbstractBaseController):
    class Meta:
        label = 'status'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Print project status'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        if self.app.pargs.fetch:
            _fetch_projects(self.clowder_repo, self.clowder)
        else:
            self.clowder_repo.print_status()

        padding = len(max(self.clowder.get_all_project_paths(), key=len))

        for group in self.clowder.groups:
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