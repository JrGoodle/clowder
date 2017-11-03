import colorama
from cement.core.foundation import CementApp

import clowder.cli as cmd


class ClowderApp(CementApp):
    class Meta:
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
    with ClowderApp() as app:
        app.run()


if __name__ == '__main__':
    colorama.init()
    main()
