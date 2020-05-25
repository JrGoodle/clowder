# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import pkg_resources
from multiprocessing import freeze_support

# noinspection PyPackageRequirements
import argcomplete
import colorama

import clowder.cli as cmd
from clowder import LOG_DEBUG
from clowder.error import ClowderConfigYAMLError, ClowderExit


class ClowderArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        # Make sure mp pool is closed
        argparse.ArgumentParser.error(self, message)

    def exit(self, status=0, message=None):
        # Make sure mp pool is closed
        if message is not None:
            message = f"{message}\n"
        else:
            print()
        argparse.ArgumentParser.exit(self, status, message)


def create_parsers() -> ClowderArgumentParser:
    parser = ClowderArgumentParser(prog='clowder')
    version_message = f"clowder version {pkg_resources.require('clowder-repo')[0].version}"
    arguments = [
        (['-v', '--version'], dict(action='version', version=version_message))
    ]
    cmd.add_parser_arguments(parser, arguments)
    subparsers = parser.add_subparsers(help='sub-command help')

    cmd.add_branch_parser(subparsers)
    cmd.add_checkout_parser(subparsers)
    cmd.add_clean_parser(subparsers)
    cmd.add_config_parser(subparsers)
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
    parser = None
    try:
        parser = create_parsers()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        args.func(args) # noqa
    except ClowderExit as err:
        LOG_DEBUG('ClowderExit exception', err)
        print()
        exit(err.code)
    except ClowderConfigYAMLError as err:
        print(err.message)
        LOG_DEBUG('ClowderConfigYAMLError exception', err)
        print()
        exit(err.code)
    except AttributeError as err:
        LOG_DEBUG('AttributeError exception', err)
        if parser is not None:
            parser.print_help()
        print()
        exit(1)
    except Exception as err: # noqa
        LOG_DEBUG('Unhandled generic exception', err)
        print()
        exit(1)


if __name__ == '__main__':
    freeze_support()
    colorama.init()
    main()
