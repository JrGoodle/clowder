"""Main entrypoint for clowder test runner"""

from __future__ import print_function
import argparse
import atexit
import os
import signal
import sys
import argcomplete
import colorama
from termcolor import cprint, colored


def main():
    """Main entrypoint for clowder test runner"""
    colorama.init()
    Command()


if __name__ == '__main__':
    raise SystemExit(main())


# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for too many branches
# pylint: disable=R0912


class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        # clowder argparse setup
        command_description = 'Clowder test runner'
        parser = argparse.ArgumentParser(description=command_description,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--python2', action='store_true',
                            help='clean all the things')
        parser.add_argument('--write', '-w', action='store_true',
                            help='clean submodules recursively')
        self._subparsers = parser.add_subparsers(dest='test_command', metavar='SUBCOMMAND')
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()
        if self.args.test_command is None or not hasattr(self, self.args.test_command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.clowder_command)()
        print()

    def branch(self):
        """clowder branch command"""
        self.args.python2
        self.args.write

    def _configure_cats_subparser(self):
        """clowder branch command"""
        cats_help = 'Run cats tests'
        parser_clean = subparsers.add_parser('clean', help=cats_help)



def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    parser.print_help()
    print()
    sys.exit(1)
