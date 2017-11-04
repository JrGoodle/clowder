# -*- coding: utf-8 -*-
"""Clowder command line repo controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_repo import (
    CLOWDER_REPO,
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch
)
from clowder.util.connectivity import network_connection_required


class RepoController(ArgparseController):
    """Clowder repo command controller"""

    class Meta:
        """Clowder repo Meta configuration"""

        label = 'repo'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Manage clowder repo'


class RepoAddController(ArgparseController):
    """Clowder repo add command controller"""

    class Meta:
        """Clowder repo add Meta configuration"""

        label = 'add'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Add files in clowder repo'

    @expose(
        help='this is the help message for clowder repo add',
        arguments=[(['files'], dict(nargs='+', metavar='FILE', help='files to add'))]
    )
    def add(self):
        """Clowder repo add command entry point"""

        self._add()

    @clowder_required
    @print_clowder_repo_status
    def _add(self):
        """Clowder repo add command private implementation"""

        CLOWDER_REPO.add(self.app.pargs.files)


class RepoCheckoutController(ArgparseController):
    """Clowder repo checkout command controller"""

    class Meta:
        """Clowder repo checkout Meta configuration"""

        label = 'checkout'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Checkout ref in clowder repo'

    @expose(
        help='this is the help message for clowder repo checkout',
        arguments=[(['ref'], dict(nargs=1, metavar='REF', help='git ref to checkout'))]
    )
    def checkout(self):
        """Clowder repo checkout command entry point"""

        self._checkout()

    @clowder_required
    @print_clowder_repo_status_fetch
    def _checkout(self):
        """Clowder repo checkout command private implementation"""

        CLOWDER_REPO.checkout(self.app.pargs.ref[0])


class RepoCleanController(ArgparseController):
    """Clowder repo clean command controller"""

    class Meta:
        """Clowder repo clean Meta configuration"""

        label = 'clean'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Discard changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo clean',
    )
    def clean(self):
        """Clowder repo clean command entry point"""

        self._clean()

    @clowder_required
    @print_clowder_repo_status
    @staticmethod
    def _clean():
        """Clowder repo clean command private implementation"""

        CLOWDER_REPO.clean()


class RepoCommitController(ArgparseController):
    """Clowder repo commit command controller"""

    class Meta:
        """Clowder repo commit Meta configuration"""

        label = 'commit'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Commit current changes in clowder repo yaml files'

    @expose(
        help='this is the help message for clowder repo commit',
        arguments=[(['message'], dict(nargs=1, metavar='MESSAGE', help='commit message'))]
    )
    def commit(self):
        """Clowder repo commit command entry point"""

        self._commit()

    @clowder_required
    @print_clowder_repo_status
    def _commit(self):
        """Clowder repo commit command private implementation"""

        CLOWDER_REPO.commit(self.app.pargs.message[0])


class RepoPullController(ArgparseController):
    """Clowder repo pull command controller"""

    class Meta:
        """Clowder repo pull Meta configuration"""

        label = 'pull'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Pull upstream changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo pull',
    )
    def pull(self):
        """Clowder repo pull command entry point"""

        self._pull()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    @staticmethod
    def _pull():
        """Clowder repo pull command private implementation"""

        CLOWDER_REPO.pull()


class RepoPushController(ArgparseController):
    """Clowder repo push command controller"""

    class Meta:
        """Clowder repo push Meta configuration"""

        label = 'push'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Push changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo push',
    )
    def push(self):
        """Clowder repo push command entry point"""

        self._push()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    @staticmethod
    def _push():
        """Clowder repo push command private implementation"""

        CLOWDER_REPO.push()


class RepoRunController(ArgparseController):
    """Clowder repo run command controller"""

    class Meta:
        """Clowder repo run Meta configuration"""

        label = 'run'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Run command in clowder repo'

    @expose(
        help='this is the help message for clowder repo add',
        arguments=[
            (['command'], dict(nargs=1, metavar='COMMAND', help='command to run in clowder repo directory'))
        ]
    )
    def run(self):
        """Clowder repo run command entry point"""

        self._run()

    @clowder_required
    @print_clowder_repo_status
    def _run(self):
        """Clowder repo run command private implementation"""

        CLOWDER_REPO.run_command(self.app.pargs.command[0])


class RepoStatusController(ArgparseController):
    """Clowder repo status command controller"""

    class Meta:
        """Clowder repo status Meta configuration"""

        label = 'status'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Print clowder repo git status'

    @expose(
        help='this is the help message for clowder repo status',
    )
    def status(self):
        """Clowder repo status command entry point"""

        self._status()

    @clowder_required
    @print_clowder_repo_status
    @staticmethod
    def _status():
        """Clowder repo status command private implementation"""

        CLOWDER_REPO.git_status()
