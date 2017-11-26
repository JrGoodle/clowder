# -*- coding: utf-8 -*-
"""Clowder command line checkout controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required
from clowder.util.clowder_utils import (
    filter_groups,
    filter_projects,
    options_help_message,
    run_group_command,
    run_project_command
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
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to checkout branches for'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to checkout branches for'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
        ]
    )
    def checkout(self):
        """Clowder checkout command entry point"""

        self._checkout()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _checkout(self):
        """Clowder checkout command private implementation"""

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'checkout', self.app.pargs.branch[0])
            return

        projects = filter_projects(CLOWDER_CONTROLLER.groups, project_names=self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'checkout', self.app.pargs.branch[0])
