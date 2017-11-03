from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


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
    def default(self):
        print("Inside SecondController.default()")
