# -*- coding: utf-8 -*-
"""Clowder command line diff controller

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
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to show diff for')))
        ]
    )
    def diff(self) -> None:
        """Clowder diff command entry point"""

        self._diff()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _diff(self) -> None:
        """Clowder diff command private implementation"""

        projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
        for project in projects:
            print(project.status())
            project.diff()
