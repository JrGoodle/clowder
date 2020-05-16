# -*- coding: utf-8 -*-
"""Clowder command line repo controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

import clowder.clowder_repo as clowder_repo
from clowder.util.decorators import (
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
        help = 'Manage clowder repo'


class RepoAddController(ArgparseController):
    """Clowder repo add command controller"""

    class Meta:
        """Clowder repo add Meta configuration"""

        label = 'add'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Add files in clowder repo'

    @expose(
        help='Add files in clowder repo',
        arguments=[(['files'], dict(nargs='+', metavar='FILE', help='files to add'))]
    )
    def add(self) -> None:
        """Clowder repo add command entry point"""

        self._add()

    @clowder_required
    @print_clowder_repo_status
    def _add(self) -> None:
        """Clowder repo add command private implementation"""

        clowder_repo.add(self.app.pargs.files)


class RepoCommitController(ArgparseController):
    """Clowder repo commit command controller"""

    class Meta:
        """Clowder repo commit Meta configuration"""

        label = 'commit'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Commit current changes in clowder repo yaml files'

    @expose(
        help='Commit current changes in clowder repo yaml files',
        arguments=[(['message'], dict(nargs=1, metavar='MESSAGE', help='commit message'))]
    )
    def commit(self) -> None:
        """Clowder repo commit command entry point"""

        self._commit()

    @clowder_required
    @print_clowder_repo_status
    def _commit(self) -> None:
        """Clowder repo commit command private implementation"""

        clowder_repo.commit(self.app.pargs.message[0])


class RepoPullController(ArgparseController):
    """Clowder repo pull command controller"""

    class Meta:
        """Clowder repo pull Meta configuration"""

        label = 'pull'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Pull upstream changes in clowder repo'

    @expose(
        help='Pull upstream changes in clowder repo'
    )
    def pull(self) -> None:
        """Clowder repo pull command entry point"""

        self._pull()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def _pull(self) -> None:
        """Clowder repo pull command private implementation"""

        clowder_repo.pull()


class RepoPushController(ArgparseController):
    """Clowder repo push command controller"""

    class Meta:
        """Clowder repo push Meta configuration"""

        label = 'push'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Push changes in clowder repo'

    @expose(
        help='Push changes in clowder repo'
    )
    def push(self) -> None:
        """Clowder repo push command entry point"""

        self._push()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def _push(self) -> None:
        """Clowder repo push command private implementation"""

        clowder_repo.push()


class RepoRunController(ArgparseController):
    """Clowder repo run command controller"""

    class Meta:
        """Clowder repo run Meta configuration"""

        label = 'run'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Run command in clowder repo'

    @expose(
        help='Run command in clowder repo',
        arguments=[
            (['command'], dict(nargs=1, metavar='COMMAND', help='command to run in clowder repo directory'))
        ]
    )
    def run(self) -> None:
        """Clowder repo run command entry point"""

        self._run()

    @clowder_required
    @print_clowder_repo_status
    def _run(self) -> None:
        """Clowder repo run command private implementation"""

        clowder_repo.run_command(self.app.pargs.command[0])


class RepoCheckoutController(ArgparseController):
    """Clowder repo checkout command controller"""

    class Meta:
        """Clowder repo checkout Meta configuration"""

        label = 'repo_checkout'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        aliases = ['checkout']
        aliases_only = True
        description = 'Checkout ref in clowder repo'

    @expose(
        arguments=[(['ref'], dict(nargs=1, metavar='REF', help='git ref to checkout'))],
        aliases=['checkout'],
        help='Checkout ref in clowder repo'
    )
    def repo_checkout(self) -> None:
        """Clowder repo checkout command entry point"""

        self._checkout()

    @clowder_required
    @print_clowder_repo_status_fetch
    def _checkout(self) -> None:
        """Clowder repo checkout command private implementation"""

        clowder_repo.checkout(self.app.pargs.ref[0])


class RepoCleanController(ArgparseController):
    """Clowder repo clean command controller"""

    class Meta:
        """Clowder repo clean Meta configuration"""

        label = 'repo_clean'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        aliases = ['clean']
        aliases_only = True
        description = 'Discard changes in clowder repo'

    @expose(
        aliases=['clean'],
        help='Discard changes in clowder repo'
    )
    def repo_clean(self) -> None:
        """Clowder repo clean command entry point"""

        self._clean()

    @clowder_required
    @print_clowder_repo_status
    def _clean(self) -> None:
        """Clowder repo clean command private implementation"""

        clowder_repo.clean()


class RepoStatusController(ArgparseController):
    """Clowder repo status command controller"""

    class Meta:
        """Clowder repo status Meta configuration"""

        label = 'repo_status'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        aliases = ['status']
        aliases_only = True
        description = 'Print clowder repo git status'

    @expose(
        aliases=['status'],
        help='Print clowder repo git status'
    )
    def repo_status(self) -> None:
        """Clowder repo status command entry point"""

        self._status()

    @clowder_required
    @print_clowder_repo_status
    def _status(self) -> None:
        """Clowder repo status command private implementation"""

        clowder_repo.git_status()
