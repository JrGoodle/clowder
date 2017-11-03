from cement.ext.ext_argparse import expose

import clowder.commands as commands
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import (
    print_clowder_repo_status_fetch,
    network_connection_required,
    valid_clowder_yaml_required
)


class HerdController(AbstractBaseController):
    class Meta:
        label = 'herd'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Clone and update projects with latest changes'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--parallel'], dict(action='store_true', help='run commands in parallel')),
            (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
            (['--depth', '-d'], dict(default=None, type=int, nargs=1, metavar='DEPTH', help='depth to herd')),
            (['--branch', '-b'], dict(nargs=1, default=None, metavar='BRANCH', help='branch to herd if present')),
            (['--tag', '-t'], dict(nargs=1, default=None, metavar='TAG', help='tag to herd if present'))
            ]

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @valid_clowder_yaml_required
    @print_clowder_repo_status_fetch
    def default(self):
        branch = None if self.app.pargs.branch is None else self.app.pargs.branch[0]
        tag = None if self.app.pargs.tag is None else self.app.pargs.tag[0]
        depth = None if self.app.pargs.depth is None else self.app.pargs.depth[0]

        kwargs = {'group_names': self.app.pargs.groups, 'project_names': self.app.pargs.projects,
                  'skip': self.app.pargs.skip, 'branch': branch, 'tag': tag,
                  'depth': depth, 'rebase': self.app.pargs.rebase}
        if self.app.pargs.parallel:
            commands.herd_parallel(self.clowder, **kwargs)
            return
        commands.herd(self.clowder, **kwargs)
