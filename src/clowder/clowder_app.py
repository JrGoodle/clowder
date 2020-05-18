# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
from multiprocessing import freeze_support

import colorama

import clowder.cli as cmd
from clowder.error import ClowderExit
from clowder.util.clowder_utils import add_parser_arguments
from clowder.util.parallel_commands import __clowder_pool__

VERSION = '3.2.0'


class ClowderArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        # Make sure mp pool is closed
        close_mp_pool()

        argparse.ArgumentParser.error(self, message)

    def exit(self, status=0, message=None):
        # Make sure mp pool is closed
        close_mp_pool()

        argparse.ArgumentParser.exit(self, status, message)


class ClowderApp(object):
    """Clowder command CLI app"""

    def create_parsers(self) -> ClowderArgumentParser:
        parser = ClowderArgumentParser(prog='clowder')
        arguments = [
            (['-v', '--version'], dict(action='version', version=VERSION)),
        ]
        add_parser_arguments(parser, arguments)
        subparsers = parser.add_subparsers(help='sub-command help')

        cmd.add_branch_parser(subparsers)
        cmd.add_checkout_parser(subparsers)
        cmd.add_clean_parser(subparsers)
        cmd.add_diff_parser(subparsers)
        cmd.add_forall_parser(subparsers)
        cmd.add_herd_parser(subparsers)
        cmd.add_init_parser(subparsers)
        cmd.add_link_parser(subparsers)
        cmd.add_prune_parser(subparsers)
        cmd.add_repo_parser(subparsers)
        cmd.add_reset_parser(subparsers)
        cmd.add_save_parser(subparsers)
        cmd.add_start_parser(subparsers)
        cmd.add_stash_parser(subparsers)
        cmd.add_status_parser(subparsers)
        cmd.add_yaml_parser(subparsers)

        return parser


def main() -> None:
    """Clowder command CLI main function"""

    print()

    app = ClowderApp()
    parser = app.create_parsers()
    args = parser.parse_args()
    if 'projects' in args:
        if isinstance(args.projects, str):
            args.projects = [args.projects]

    exit_code = 0
    try:
        args.func(args) # noqa
    except ClowderExit as err:
        exit_code = err.code
    except AttributeError:
        exit_code = 1
        parser.print_help()
    finally:
        print()

        # Make sure mp pool is closed
        close_mp_pool()

        exit(exit_code)


def close_mp_pool():
    try:
        __clowder_pool__.close()
        __clowder_pool__.join()
    except:  # noqa
        __clowder_pool__.terminate()

if __name__ == '__main__':
    freeze_support()
    colorama.init()
    main()
