"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
import pkg_resources
from typing import Optional

import argcomplete
import colorama

import clowder.cli as cmd
import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG


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
#             CONSOLE.print()
#         argparse.ArgumentParser.exit(self, status, message)


clowder_parser: Optional[argparse.ArgumentParser] = None


def clowder_help(args):  # noqa
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
        subparsers = clowder_parser.add_subparsers(dest='subcommand', help='sub-command help')

        cmd.add_branch_parser(subparsers)
        cmd.add_checkout_parser(subparsers)
        cmd.add_clean_parser(subparsers)
        cmd.add_config_parser(subparsers)
        cmd.add_diff_parser(subparsers)
        cmd.add_forall_parser(subparsers)
        cmd.add_herd_parser(subparsers)
        cmd.add_init_parser(subparsers)
        cmd.add_link_parser(subparsers)
        cmd.add_plugins_parser(subparsers)
        cmd.add_prune_parser(subparsers)
        cmd.add_repo_parser(subparsers)
        cmd.add_reset_parser(subparsers)
        cmd.add_save_parser(subparsers)
        cmd.add_start_parser(subparsers)
        cmd.add_stash_parser(subparsers)
        cmd.add_status_parser(subparsers)
        cmd.add_yaml_parser(subparsers)
    except Exception as err:
        LOG.error('Failed to create parser', err)
        CONSOLE.print(fmt.error_failed_create_parser())
        raise
    else:
        return clowder_parser


def main() -> None:
    """Clowder command CLI main function"""

    CONSOLE.print()
    try:
        parser = create_parsers()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        args.func(args)
    except ClowderError as err:
        LOG.debug('** ClowderError **', err)
        CONSOLE.print_exception()
        if err.exit_code is not None:
            exit(err.exit_code)
        exit(err.error_type.value)
    except SystemExit as err:
        if err.code == 0:
            print()
            exit()
        LOG.debug('** SystemExit **', err)
        CONSOLE.print_exception()
        exit(err.code)
    except KeyboardInterrupt as err:
        LOG.debug('** KeyboardInterrupt **', err)
        CONSOLE.print()
        exit(ClowderErrorType.USER_INTERRUPT.value)
    except Exception as err:
        LOG.debug('** Unhandled exception **', err)
        CONSOLE.print_exception()
        exit(ClowderErrorType.UNKNOWN.value)
    else:
        CONSOLE.print()


if __name__ == '__main__':
    # from rich.traceback import install
    # install()
    colorama.init()
    main()
