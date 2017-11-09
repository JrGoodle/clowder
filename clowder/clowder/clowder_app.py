# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

import colorama
from cement.core.foundation import CementApp

import clowder.cli as cmd
from clowder.error.clowder_exit import ClowderExit


class ClowderApp(CementApp):
    """Clowder command CLI app"""

    class Meta:
        """Clowder command CLI Meta configuration"""

        label = 'clowder'
        extensions = ['argcomplete']
        base_controller = 'base'
        handlers = [
            cmd.BaseController,
            cmd.BranchController,
            cmd.CheckoutController,
            cmd.CleanController,
            cmd.DiffController,
            cmd.ForallController,
            cmd.HerdController,
            cmd.InitController,
            cmd.LinkController,
            cmd.PruneController,
            cmd.RepoController,
            cmd.RepoAddController,
            # cmd.RepoCheckoutController,
            # cmd.RepoCleanController,
            cmd.RepoCommitController,
            cmd.RepoRunController,
            cmd.RepoPullController,
            cmd.RepoPushController,
            # cmd.RepoStatusController,
            cmd.ResetController,
            cmd.SaveController,
            cmd.StartController,
            cmd.StashController,
            cmd.StatusController,
            cmd.SyncController,
            cmd.YAMLController
            ]


def main():
    """Clowder command CLI main function"""

    print()
    with ClowderApp() as app:
        try:
            app.run()
        except ClowderExit:
            sys.tracebacklimit = 0
            raise
        print()


if __name__ == '__main__':
    colorama.init()
    main()
