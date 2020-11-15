"""Clowder command line app

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import argparse
import pkg_resources
import sys
from subprocess import CalledProcessError

import argcomplete
import colorama

import clowder.cli as cmd
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
#             CONSOLE.stdout()
#         argparse.ArgumentParser.exit(self, status, message)


def create_parsers() -> argparse.ArgumentParser:
    """Configure clowder CLI parsers

    :return: Configured argument parser for clowder command
    :rtype: argparse.ArgumentParser
    """

    def clowder_help(args):  # noqa
        """Clowder help handler"""

        clowder_parser.print_help(file=sys.stderr)

    try:
        clowder_parser = argparse.ArgumentParser(prog='clowder')
        clowder_parser.set_defaults(func=clowder_help)
        version_message = f"clowder version {pkg_resources.require('clowder-repo')[0].version}"
        arguments = [
            (['-v', '--version'], dict(action='version', version=version_message)),
            (['--debug', '-d'], dict(action='store_true', help='print debug output')),
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
    except Exception:
        LOG.error("Failed to create command line parsers")
        raise
    else:
        return clowder_parser


def main() -> None:
    """Clowder command CLI main function"""

    CONSOLE.stdout()
    try:
        parser = create_parsers()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        if 'projects' in args:
            if isinstance(args.projects, str):
                args.projects = [args.projects]
        if args.debug:
            LOG.level = LOG.DEBUG
        args.func(args)
    except ClowderError as err:
        LOG.error(error=err)
        exit(err.error_type.value)
    except CalledProcessError as err:
        LOG.error(error=err)
        exit(err.returncode)
    except SystemExit as err:
        if err.code == 0:
            CONSOLE.stdout()
            exit()
        LOG.error(error=err)
        exit(err.code)
    except KeyboardInterrupt:
        LOG.error('** KeyboardInterrupt **\n')
        exit(ClowderErrorType.USER_INTERRUPT.value)
    except BaseException as err:
        LOG.error(error=err)
        exit(ClowderErrorType.UNKNOWN.value)
    else:
        CONSOLE.stdout()


if __name__ == '__main__':
    from rich.traceback import install
    install()
    colorama.init()
    main()
