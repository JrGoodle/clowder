# -*- coding: utf-8 -*-
"""Clowder command line repo controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_repo import (
    CLOWDER_REPO,
    clowder_required,
    print_clowder_repo_status,
    print_clowder_repo_status_fetch
)
from clowder.util.decorators import network_connection_required


class RepoController(ArgparseController):
    class Meta:
        label = 'repo'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Manage clowder repo'


class RepoAddController(ArgparseController):
    class Meta:
        label = 'add'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Add files in clowder repo'

    @expose(
        help='this is the help message for clowder repo add',
        arguments=[(['files'], dict(nargs='+', metavar='FILE', help='files to add'))]
    )
    def add(self):
        self._add()

    @clowder_required
    @print_clowder_repo_status
    def _add(self):
        CLOWDER_REPO.add(self.app.pargs.files)


class RepoCheckoutController(ArgparseController):
    class Meta:
        label = 'checkout'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Checkout ref in clowder repo'

    @expose(
        help='this is the help message for clowder repo checkout',
        arguments=[(['ref'], dict(nargs=1, metavar='REF', help='git ref to checkout'))]
    )
    def checkout(self):
        self._checkout()

    @clowder_required
    @print_clowder_repo_status_fetch
    def _checkout(self):
        CLOWDER_REPO.checkout(self.app.pargs.ref[0])


class RepoCleanController(ArgparseController):
    class Meta:
        label = 'clean'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Discard changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo clean',
    )
    def clean(self):
        self._clean()

    @clowder_required
    @print_clowder_repo_status
    def _clean(self):
        CLOWDER_REPO.clean()


class RepoCommitController(ArgparseController):
    class Meta:
        label = 'commit'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Commit current changes in clowder repo yaml files'

    @expose(
        help='this is the help message for clowder repo commit',
        arguments=[(['message'], dict(nargs=1, metavar='MESSAGE', help='commit message'))]
    )
    def commit(self):
        self._commit()

    @clowder_required
    @print_clowder_repo_status
    def _commit(self):
        CLOWDER_REPO.commit(self.app.pargs.message[0])


class RepoPullController(ArgparseController):
    class Meta:
        label = 'pull'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Pull upstream changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo pull',
    )
    def pull(self):
        self._pull()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def _pull(self):
        CLOWDER_REPO.pull()


class RepoPushController(ArgparseController):
    class Meta:
        label = 'push'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Push changes in clowder repo'

    @expose(
        help='this is the help message for clowder repo push',
    )
    def push(self):
        self._push()

    @network_connection_required
    @clowder_required
    @print_clowder_repo_status_fetch
    def _push(self):
        CLOWDER_REPO.push()


class RepoRunController(ArgparseController):
    class Meta:
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
        self._run()

    @clowder_required
    @print_clowder_repo_status
    def _run(self):
        CLOWDER_REPO.run_command(self.app.pargs.command[0])


class RepoStatusController(ArgparseController):
    class Meta:
        label = 'status'
        stacked_on = 'repo'
        stacked_type = 'embedded'
        description = 'Print clowder repo git status'

    @expose(
        help='this is the help message for clowder repo status',
    )
    def status(self):
        self._status()

    @clowder_required
    @print_clowder_repo_status
    def _status(self):
        CLOWDER_REPO.git_status()
