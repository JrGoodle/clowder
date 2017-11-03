from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class InitController(AbstractBaseController):
    class Meta:
        label = 'init'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Clone repository to clowder directory and create clowder.yaml symlink'
        arguments = [
            (['url'], dict(metavar='URL', help='url of repo containing clowder.yaml')),
            (['--branch', '-b'], dict(nargs=1, metavar='BRANCH', help='branch of repo containing clowder.yaml'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
