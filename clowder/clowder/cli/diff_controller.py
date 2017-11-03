# -*- coding: utf-8 -*-
"""Clowder command line diff controller

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


class DiffController(ArgparseController):
    class Meta:
        label = 'diff'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Show git diff for projects'

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, [], 'diff')
            return

        projects = filter_projects_on_project_names(CLOWDER_CONTROLLER.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, [], 'diff')
