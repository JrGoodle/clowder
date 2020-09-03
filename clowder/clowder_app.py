# -*- coding: utf-8 -*-
"""Clowder command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse
import pkg_resources
from multiprocessing import freeze_support
from typing import Optional

# noinspection PyPackageRequirements
import argcomplete
import colorama

import clowder.cli as cmd
import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG


# class ClowderArgumentParser(argparse.ArgumentParser):
#     """Custom argument parser subclass"""
#
#     def error(self, message):
#         argparse.ArgumentParser.error(self, message)
#
#     def exit(self, status=0, message=None):
#         if message is not None:
#             message = f"{message}\n"
#         else:
#             print()
#         argparse.ArgumentParser.exit(self, status, message)


clowder_parser: Optional[argparse.ArgumentParser] = None


def clowder_help(args): # noqa
    """Clowder help handler"""

    clowder_parser.print_help()


def create_parsers() -> argparse.ArgumentParser:
    """Configure clowder CLI parsers

    :return: Configured argument parser for clowder command
    :rtype: argparse.ArgumentParser
    """
    try:
        global clowder_parser
        clowder_parser = argparse.ArgumentParser(prog='clowder')
        clowder_parser.set_defaults(func=clowder_help)
        version_message = f"clowder version {pkg_resources.require('clowder-repo')[0].version}"
        arguments = [
            (['-v', '--version'], dict(action='version', version=version_message))
        ]
        cmd.add_parser_arguments(clowder_parser, arguments)
        subparsers = clowder_parser.add_subparsers(help='sub-command help')

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
    except Exception as err:
        LOG_DEBUG('Failed to create parser', err)
        raise ClowderError(ClowderErrorType.PARSER_CREATION_FAILED, fmt.error_failed_create_parser())
    else:
        return clowder_parser


def main() -> None:
    """Clowder command CLI main function"""

    print()
    try:
        parser = create_parsers()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        args.func(args)
    except ClowderError as err:
        LOG_DEBUG('** ClowderError **', err)
        print(err)
        print()
        if err.exit_code is not None:
            exit(err.exit_code)
        else:
            exit(err.error_type.value)
    except SystemExit as err:
        LOG_DEBUG('** SystemExit **', err)
        print()
        exit(err.code)
    except KeyboardInterrupt as err:
        LOG_DEBUG('** KeyboardInterrupt **', err)
        print(fmt.error_user_interrupt())
        print()
        exit(ClowderErrorType.USER_INTERRUPT.value)
    except Exception as err:
        LOG_DEBUG('** Unhandled exception **', err)
        print(fmt.error_unknown_error())
        print()
        exit(ClowderErrorType.UNKNOWN.value)
    else:
        print()


if __name__ == '__main__':
    freeze_support()
    colorama.init()
    main()
