# -*- coding: utf-8 -*-
"""Clowder command line herd controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli.parallel import (
    herd,
    herd_parallel
)
from clowder.clowder_repo import (
    print_clowder_repo_status_fetch,
    valid_clowder_yaml_required
)
from clowder.cli.globals import CLOWDER_CONTROLLER
from clowder.util.decorators import network_connection_required


class HerdController(ArgparseController):
    class Meta:
        label = 'herd'
        stacked_on = 'base'
        stacked_type = 'embedded'
        description = 'Clone and update projects with latest changes'

    @expose(
        help='this is the help message for clowder herd',
        arguments=[
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
            (['--depth', '-d'], dict(default=None, type=int, nargs=1, metavar='DEPTH', help='depth to herd')),
            (['--branch', '-b'], dict(nargs=1, default=None, metavar='BRANCH', help='branch to herd if present')),
            (['--tag', '-t'], dict(nargs=1, default=None, metavar='TAG', help='tag to herd if present')),
            (['--groups', '-g'], dict(choices=CLOWDER_CONTROLLER.get_all_group_names(),
                                      default=CLOWDER_CONTROLLER.get_all_group_names(),
                                      nargs='+', metavar='GROUP', help='groups to herd')),
            (['--projects', '-p'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                        nargs='+', metavar='PROJECT', help='projects to herd')),
            (['--skip', '-s'], dict(choices=CLOWDER_CONTROLLER.get_all_project_names(),
                                    nargs='+', metavar='PROJECT', default=[], help='projects to skip'))
            ]
    )
    def herd(self):
        self._herd()

    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def _herd(self):
        branch = None if self.app.pargs.branch is None else self.app.pargs.branch[0]
        tag = None if self.app.pargs.tag is None else self.app.pargs.tag[0]
        depth = None if self.app.pargs.depth is None else self.app.pargs.depth[0]

        kwargs = {'group_names': self.app.pargs.groups, 'project_names': self.app.pargs.projects,
                  'skip': self.app.pargs.skip, 'branch': branch, 'tag': tag,
                  'depth': depth, 'rebase': self.app.pargs.rebase}
        if self.app.pargs.parallel:
            herd_parallel(CLOWDER_CONTROLLER, **kwargs)
            return
        herd(CLOWDER_CONTROLLER, **kwargs)
