# -*- coding: utf-8 -*-
"""Clowder command line checkout controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    filter_projects,
    options_help_message
)


class CheckoutController(ArgparseController):
    """Clowder checkout command controller"""

    class Meta:
        """Clowder checkout Meta configuration"""

        label = 'checkout'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Checkout local branch in projects'

    @expose(
        help='Checkout local branch in projects',
        arguments=[
            (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='BRANCH')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to checkout branches for')))
        ]
    )
    def checkout(self) -> None:
        """Clowder checkout command entry point"""

        self._checkout()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _checkout(self) -> None:
        """Clowder checkout command private implementation"""

        projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
        for project in projects:
            print(project.status())
            project.checkout(self.app.pargs.branch[0])
