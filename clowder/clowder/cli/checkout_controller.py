# -*- coding: utf-8 -*-
"""Clowder command line checkout controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
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


class CheckoutController(AbstractBaseController):
    class Meta:
        label = 'checkout'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Checkout local branch in projects'

    @expose(
        help='this is the help message for clowder checkout',
        arguments=AbstractBaseController.Meta.arguments + [
            (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='BRANCH'))
        ]
    )
    def checkout(self):
        self._checkout()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _checkout(self):
        if self.app.pargs.projects is None:
            groups = filter_groups(self.clowder.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'checkout', self.app.pargs.branch[0])
            return

        projects = filter_projects_on_project_names(self.clowder.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'checkout', self.app.pargs.branch[0])