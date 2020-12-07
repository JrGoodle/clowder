"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App, Argument

import clowder.cli as cli
from clowder.log import LOG


def main() -> None:
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
    arguments = [
        Argument('--debug', '-d', action='store_true', help='print debug output')
    ]
    app = App('clowder-repo', entry_point='clowder', arguments=arguments, subcommands=subcommands)

    def process_args(args) -> None:
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        if args.debug:
            LOG.level = LOG.DEBUG

    app.run(process_args)


if __name__ == '__main__':
    main()
