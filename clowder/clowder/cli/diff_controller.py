# -*- coding: utf-8 -*-
"""Clowder command line diff controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import (
    filter_groups,
    filter_projects_on_project_names,
    options_help_message,
    run_group_command,
    run_project_command
)
from clowder.clowder_repo import print_clowder_repo_status
from clowder.util.decorators import valid_clowder_yaml_required


class DiffController(ArgparseController):
    """Clowder diff command controller"""

    class Meta:
        """Clowder diff Meta configuration"""

        label = 'diff'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Show git diff for projects'

    @expose(
        help='Show git diff for projects',
        arguments=[
            (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='BRANCH')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to show diff for'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to show diff for'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
        ]
    )
    def diff(self):
        """Clowder diff command entry point"""

        self._diff()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _diff(self):
        """Clowder diff command private implementation"""

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, [], 'diff')
            return

        projects = filter_projects_on_project_names(CLOWDER_CONTROLLER.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, [], 'diff')
