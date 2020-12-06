"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App

import clowder.cli as cmd
from clowder.log import LOG


def main() -> None:
    subcommands = [
        cmd.branch.add_parser,
        cmd.checkout.add_parser,
        cmd.clean.add_parser,
        cmd.config.add_parser,
        cmd.diff.add_parser,
        cmd.forall.add_parser,
        cmd.herd.add_parser,
        cmd.init.add_parser,
        cmd.link.add_parser,
        cmd.plugins.add_parser,
        cmd.prune.add_parser,
        cmd.repo.add_parser,
        cmd.reset.add_parser,
        cmd.save.add_parser,
        cmd.start.add_parser,
        cmd.stash.add_parser,
        cmd.status.add_parser,
        cmd.yaml.add_parser
    ]
    arguments = [
        (['--debug', '-d'], dict(action='store_true', help='print debug output'))
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
