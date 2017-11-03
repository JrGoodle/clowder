# -*- coding: utf-8 -*-
"""Clowder command line branch controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_repo import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


class BranchController(ArgparseController):
    class Meta:
        label = 'branch'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Display current branches'

    @expose(
        help='this is the help message for clowder branch',
        arguments=[
            (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
            ]
    )
    def branch(self):
        self._branch()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _branch(self):
        local = True
        remote = False
        if self.app.pargs.all:
            local = True
            remote = True
        elif self.app.pargs.remote:
            remote = True

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'branch', local=local, remote=remote)
            return

        projects = filter_projects_on_project_names(CLOWDER_CONTROLLER.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'branch', local=local, remote=remote)
