# -*- coding: utf-8 -*-
"""Clowder command line diff controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_repo import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.cli.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)


class DiffController(ArgparseController):
    class Meta:
        label = 'diff'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Show git diff for projects'

    @expose(
        help='this is the help message for clowder diff',
        arguments=[
            (['branch'], dict(nargs=1, action='store', help='branch to checkout', metavar='BRANCH')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT', help='projects to herd')),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[], help='projects to skip'))
        ]
    )
    def diff(self):
        self._diff()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _diff(self):
        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, [], 'diff')
            return

        projects = filter_projects_on_project_names(CLOWDER_CONTROLLER.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, [], 'diff')
