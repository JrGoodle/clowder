# -*- coding: utf-8 -*-
"""Clowder command line stash controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli import CLOWDER_CONTROLLER
from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


class StashController(ArgparseController):
    class Meta:
        label = 'stash'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Stash current changes'
        arguments = [
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT', help='projects to herd')),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[], help='projects to skip'))
        ]

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        if not any([g.is_dirty() for g in CLOWDER_CONTROLLER.groups]):
            print('No changes to stash')
            return

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'stash')
            return

        projects = filter_projects_on_project_names(CLOWDER_CONTROLLER.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'stash')
