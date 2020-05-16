# -*- coding: utf-8 -*-
"""Clowder command line branch controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
)


class BranchController(ArgparseController):
    """Clowder branch command controller"""

    class Meta:
        """Clowder branch Meta configuration"""

        label = 'branch'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Display current branches'

    @expose(
        help='Display current branches',
        arguments=[
            (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='show remote branches')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to show branches for')))
            ]
    )
    def branch(self) -> None:
        """Clowder branch command entry point"""
        self._branch()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _branch(self) -> None:
        """Clowder branch command private implementation"""
        local = True
        remote = False
        if self.app.pargs.all:
            local = True
            remote = True
        elif self.app.pargs.remote:
            remote = True

        projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
        for project in projects:
            print(project.status())
            project.branch(local=local, remote=remote)
