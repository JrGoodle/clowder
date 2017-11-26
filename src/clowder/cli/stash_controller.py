# -*- coding: utf-8 -*-
"""Clowder command line stash controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

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
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP',
                                      help=options_help_message(CLOWDER_CONTROLLER.get_all_group_names(),
                                                                'groups to stash'))),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT',
                                        help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                                  'projects to stash'))),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[],
                                    help=options_help_message(CLOWDER_CONTROLLER.get_all_project_names(),
                                                              'projects to skip')))
        ]
    )
    def stash(self):
        """Clowder stash command entry point"""

        self._stash()

    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def _stash(self):
        """Clowder stash command private implementation"""

        if not any([g.is_dirty() for g in CLOWDER_CONTROLLER.groups]):
            print('No changes to stash')
            return

        if self.app.pargs.projects is None:
            groups = filter_groups(CLOWDER_CONTROLLER.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'stash')
            return

        projects = filter_projects(CLOWDER_CONTROLLER.groups, project_names=self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'stash')
