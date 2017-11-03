# -*- coding: utf-8 -*-
"""Clowder command line repo controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.cli import CLOWDER_REPO
from clowder.util.decorators import (
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch,
    network_connection_required
)


class RepoController(ArgparseController):
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


class RepoAddController(ArgparseController):
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
        CLOWDER_REPO.add(self.app.pargs.files)


class RepoCheckoutController(ArgparseController):
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
        CLOWDER_REPO.checkout(self.app.pargs.ref[0])


class RepoCleanController(ArgparseController):
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
        CLOWDER_REPO.clean()


class RepoCommitController(ArgparseController):
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
        CLOWDER_REPO.commit(self.app.pargs.message[0])


class RepoPullController(ArgparseController):
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
        CLOWDER_REPO.pull()


class RepoPushController(ArgparseController):
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
        CLOWDER_REPO.push()


class RepoRunController(ArgparseController):
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
        CLOWDER_REPO.run_command(self.app.pargs.command[0])


class RepoStatusController(ArgparseController):
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
        CLOWDER_REPO.git_status()
