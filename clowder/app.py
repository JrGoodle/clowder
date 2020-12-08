"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App, BoolArgument

import clowder.cli as cli
from clowder.log import LOG


class ClowderApp(App):
    class Meta:
        name = 'clowder-repo'
        entry_point = 'clowder'
        arguments = [
            BoolArgument('--debug', '-d', help='print debug output')
        ]
        subcommands = [
            cli.BranchCommand(),
            cli.CheckoutCommand(),
            cli.CleanCommand(),
            cli.ConfigCommand(),
            cli.DiffCommand(),
            cli.ForallCommand(),
            cli.HerdCommand(),
            cli.InitCommand(),
            cli.LinkCommand(),
            cli.PruneCommand(),
            cli.RepoCommand(),
            cli.ResetCommand(),
            cli.SaveCommand(),
            cli.StartCommand(),
            cli.StashCommand(),
            cli.StatusCommand(),
            cli.YamlCommand()
        ]

    def process_args(self) -> None:
        if 'projects' in self.parsed_args:
            if isinstance(self.parsed_args.projects, str):
                self.parsed_args.projects = [self.parsed_args.projects]
        if self.parsed_args.debug:
            LOG.level = LOG.DEBUG


if __name__ == '__main__':
    ClowderApp().main()
