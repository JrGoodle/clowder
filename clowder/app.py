"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App

import clowder.cli as cmd
from clowder.log import LOG


def main() -> None:
    subcommands = [
        cmd.branch,
        cmd.checkout,
        cmd.clean,
        cmd.config,
        cmd.diff,
        cmd.forall,
        cmd.herd,
        cmd.init,
        cmd.link,
        cmd.plugins,
        cmd.prune,
        cmd.repo,
        cmd.reset,
        cmd.save,
        cmd.start,
        cmd.stash,
        cmd.status,
        cmd.yaml
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
