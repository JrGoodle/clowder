"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pygoodle.app import App

import clowder.cli as cmd
from clowder.log import LOG


def main() -> None:
    subcommands = [
        cmd.add_branch_parser,
        cmd.add_checkout_parser,
        cmd.add_clean_parser,
        cmd.add_config_parser,
        cmd.add_diff_parser,
        cmd.add_forall_parser,
        cmd.add_herd_parser,
        cmd.add_init_parser,
        cmd.add_link_parser,
        cmd.add_plugins_parser,
        cmd.add_prune_parser,
        cmd.add_repo_parser,
        cmd.add_reset_parser,
        cmd.add_save_parser,
        cmd.add_start_parser,
        cmd.add_stash_parser,
        cmd.add_status_parser,
        cmd.add_yaml_parser
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
