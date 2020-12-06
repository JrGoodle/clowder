"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App
from pygoodle.logging import Log

import clowder.cli as cmd

LOG = Log('CLOWDER')


def main() -> None:
    app = App('clowder-repo', entry_point='clowder')
    cmd.add_branch_parser(app.subparsers)
    cmd.add_checkout_parser(app.subparsers)
    cmd.add_clean_parser(app.subparsers)
    cmd.add_config_parser(app.subparsers)
    cmd.add_diff_parser(app.subparsers)
    cmd.add_forall_parser(app.subparsers)
    cmd.add_herd_parser(app.subparsers)
    cmd.add_init_parser(app.subparsers)
    cmd.add_link_parser(app.subparsers)
    cmd.add_plugins_parser(app.subparsers)
    cmd.add_prune_parser(app.subparsers)
    cmd.add_repo_parser(app.subparsers)
    cmd.add_reset_parser(app.subparsers)
    cmd.add_save_parser(app.subparsers)
    cmd.add_start_parser(app.subparsers)
    cmd.add_stash_parser(app.subparsers)
    cmd.add_status_parser(app.subparsers)
    cmd.add_yaml_parser(app.subparsers)

    def process_args(args) -> None:
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        if args.debug:
            LOG.level = LOG.DEBUG

    app.run(process_args)


if __name__ == '__main__':
    main()
