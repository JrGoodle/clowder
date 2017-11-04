# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

import colorama
from cement.core.exc import FrameworkError, CaughtSignal
from cement.core.foundation import CementApp

import clowder.cli as cmd


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
        except CaughtSignal as e:
            # determine what the signal is, and do something with it?
            from signal import SIGINT, SIGABRT

            if e.signum == SIGINT:
                # do something... maybe change the exit code?
                app.exit_code = 110
            elif e.signum == SIGABRT:
                # do something else...
                app.exit_code = 111
        except FrameworkError:
            # do something when a framework error happens
            # print("FrameworkError => %s" % e)

            # and maybe set the exit code to something unique as well
            # app.exit_code = 300

            app.args.print_help()
            sys.exit(1)
        finally:
            # Maybe we want to see a full-stack trace for the above
            # exceptions, but only if --debug was passed?
            if app.debug:
                import traceback
                traceback.print_exc()
            print()


if __name__ == '__main__':
    colorama.init()
    main()
