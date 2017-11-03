import sys

from cement.ext.ext_argparse import expose
from termcolor import colored, cprint

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import network_connection_required


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
    @network_connection_required
    def default(self):
        if self.clowder_repo:
            cprint('Clowder already initialized in this directory\n', 'red')
            sys.exit(1)

        url_output = colored(self.app.pargs.url, 'green')
        print('Create clowder repo from ' + url_output + '\n')
        if self.app.pargs.branch is None:
            branch = 'master'
        else:
            branch = str(self.app.pargs.branch[0])
        self.clowder_repo.init(self.app.pargs.url, branch)
