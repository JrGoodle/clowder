from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch,
    network_connection_required
)


class RepoController(AbstractBaseController):
    class Meta:
        label = 'repo'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Manage clowder repo'
        arguments = []

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    def default(self):
        print("Inside SecondController.default()")


class RepoAddController(AbstractBaseController):
    class Meta:
        label = 'add'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Add files in clowder repo'
        arguments = [(['files'], dict(nargs='+', metavar='FILE', help='files to add'))]

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        self.clowder_repo.add(self.app.pargs.files)


class RepoCheckoutController(AbstractBaseController):
    class Meta:
        label = 'checkout'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Checkout ref in clowder repo'
        arguments = [(['ref'], dict(nargs=1, metavar='REF', help='git ref to checkout'))]

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status_fetch
    def default(self):
        self.clowder_repo.checkout(self.app.pargs.ref[0])


class RepoCleanController(AbstractBaseController):
    class Meta:
        label = 'clean'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Discard changes in clowder repo'
        arguments = []

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        self.clowder_repo.clean()


class RepoCommitController(AbstractBaseController):
    class Meta:
        label = 'commit'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Commit current changes in clowder repo yaml files'
        arguments = [(['message'], dict(nargs=1, metavar='MESSAGE', help='commit message'))]

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        self.clowder_repo.commit(self.app.pargs.message[0])


class RepoPullController(AbstractBaseController):
    class Meta:
        label = 'pull'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Pull upstream changes in clowder repo'
        arguments = []

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def default(self):
        self.clowder_repo.pull()


class RepoPushController(AbstractBaseController):
    class Meta:
        label = 'push'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Push changes in clowder repo'
        arguments = []

    @expose(help="second-controller default command", hide=True)
    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def default(self):
        self.clowder_repo.push()


class RepoRunController(AbstractBaseController):
    class Meta:
        label = 'run'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Run command in clowder repo'
        arguments = [(['command'], dict(nargs=1, metavar='COMMAND', help='command to run in clowder repo directory'))]

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        self.clowder_repo.run_command(self.app.pargs.command[0])


class RepoStatusController(AbstractBaseController):
    class Meta:
        label = 'status'
        stacked_on = 'repo'
        stacked_type = 'nested'
        description = 'Print clowder repo git status'
        arguments = []

    @expose(help="second-controller default command", hide=True)
    @clowder_required
    @print_clowder_repo_status
    def default(self):
        self.clowder_repo.git_status()
