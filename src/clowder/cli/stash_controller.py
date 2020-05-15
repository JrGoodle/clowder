# -*- coding: utf-8 -*-
"""Clowder command line stash controller

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


class StashController(ArgparseController):
    """Clowder stash command controller"""

    class Meta:
        """Clowder stash Meta configuration"""

        label = 'stash'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Stash current changes'

    @expose(
        help='Stash current changes',
        arguments=[
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        default=['all'], nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to stash')))
        ]
    )
    def stash(self) -> None:
        """Clowder stash command entry point"""

        self._stash()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _stash(self) -> None:
        """Clowder stash command private implementation"""

        if not any([p.is_dirty() for p in CLOWDER_CONTROLLER.projects]):
            print('No changes to stash')
            return

        projects = filter_projects(CLOWDER_CONTROLLER.projects, self.app.pargs.projects)
        for project in projects:
            print(project.status())
            project.stash()
