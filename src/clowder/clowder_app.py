# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys
from multiprocessing import freeze_support

import colorama
from cement.core.exc import FrameworkError, CaughtSignal
from cement.core.foundation import CementApp

import clowder.cli as cmd
from clowder.error.clowder_exit import ClowderExit


class ClowderApp(CementApp):
    """Clowder command CLI app"""

    class Meta:
        """Clowder command CLI Meta configuration"""

        label = 'clowder'
        exit_on_close = True
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
            cmd.RepoCommitController,
            cmd.RepoRunController,
            cmd.RepoPullController,
            cmd.RepoPushController,
            cmd.ResetController,
            cmd.SaveController,
            cmd.StartController,
            cmd.StashController,
            cmd.StatusController,
            cmd.SyncController,
            cmd.YAMLController
            ]

        # Add commands that are only available on Python 3+
        if sys.version_info[0] >= 3:
            alias_handlers = [
                cmd.RepoCheckoutController,
                cmd.RepoCleanController,
                cmd.RepoStatusController
            ]
            handlers = handlers + alias_handlers


def main():
    """Clowder command CLI main function"""

    print()
    with ClowderApp() as app:
        try:
            app.run()
        except CaughtSignal as err:
            # determine what the signal is, and do something with it?
            from signal import SIGINT, SIGABRT

            if err.signum == SIGINT:
                # do something... maybe change the exit code?
                app.exit_code = 110
            elif err.signum == SIGABRT:
                # do something else...
                app.exit_code = 111
        except FrameworkError as err:
            # do something when a framework error happens
            app.args.print_help()

            # and maybe set the exit code to something unique as well
            app.exit_code = 300
        except ClowderExit as err:
            app.exit_code = err.code
        finally:
            # Maybe we want to see a full-stack trace for the above
            # exceptions, but only if --debug was passed?
            print()
            if app.debug:
                import traceback
                traceback.print_exc()


if __name__ == '__main__':
    freeze_support()
    colorama.init()
    main()
