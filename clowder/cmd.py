#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse, colorama, os, signal, sys
from termcolor import cprint
from clowder.model.clowder_repo import ClowderRepo
from clowder.model.clowder_yaml import ClowderYAML
from clowder.utility.print_utilities import (
    print_clowder_not_found_message
)

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        self.clowder = None
        self.versions = None
        self.group_names = ''
        # Load current clowder.yml config if it exists
        if os.path.isdir(os.path.join(self.root_directory, 'clowder')):
            self.clowder = ClowderYAML(self.root_directory)
            self.versions = self.clowder.get_fixed_version_names()
            if self.clowder.group_names is not None:
                self.group_names = self.clowder.group_names
        # clowder argparse setup
        command_description = 'Utility for managing multiple git repositories'
        parser = argparse.ArgumentParser(description=command_description)
        subparsers = parser.add_subparsers(dest='command')
        self._configure_subparsers(subparsers)
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        print('')
        if not hasattr(self, self.args.command):
            exit_unrecognized_command(parser)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()
        print('')

    def _configure_subparsers(self, subparsers):
        """Configure all clowder command subparsers and arguments"""
        # clowder breed
        breed_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
        parser_breed = subparsers.add_parser('breed', help=breed_help)
        parser_breed.add_argument('url', help='URL of repo containing clowder.yaml')
        # clowder herd
        herd_help = 'Clone and sync latest changes for projects'
        parser_herd = subparsers.add_parser('herd', help=herd_help)
        group = parser_herd.add_mutually_exclusive_group()
        group.add_argument('--version', '-v', choices=self.versions,
                           help='Version name to herd')
        group.add_argument('--groups', '-g', choices=self.group_names,
                           nargs='+', help='Groups to herd')
        # clowder forall
        forall_help = 'Run command in all clowder projects'
        parser_forall = subparsers.add_parser('forall', help=forall_help)
        forall_cmd_help = 'Command to run in clowder projects'
        parser_forall.add_argument('--command', '-c', dest='cmd', required=True,
                                   help=forall_cmd_help)
        parser_forall.add_argument('--groups', '-g', choices=self.group_names,
                                   nargs='+', help='Groups to herd')
        # clowder meow
        parser_meow = subparsers.add_parser('meow', add_help=False,
                                            help='Print status for projects')
        parser_meow.add_argument('--verbose', '-v', action='store_true',
                                 help='Print detailed diff status')
        # clowder fix
        fix_help = 'Create version of clowder.yaml for current repos'
        parser_fix = subparsers.add_parser('fix', help=fix_help)
        parser_fix.add_argument('-version', '-v',
                                required=True, help='Version name to fix')
        # clowder groom
        groom_help = 'Discard current changes in all projects and clowder repo'
        subparsers.add_parser('groom', add_help=False, help=groom_help)
        # clowder stash
        stash_help = 'Stash current changes in all projects and clowder repo'
        subparsers.add_parser('stash', add_help=False, help=stash_help)
        # clowder sync
        subparsers.add_parser('sync', add_help=False, help='Sync clowder repo')

    def breed(self):
        """clowder breed command"""
        if self.clowder is None:
            cprint('Breed from %s\n' % self.args.url, 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.breed(self.args.url)
        else:
            cprint('Clowder already bred in this directory, exiting...\n', 'red')
            sys.exit()

    def fix(self):
        """clowder fix command"""
        if self.clowder is not None:
            cprint('Fix...\n', 'yellow')
            self.clowder.fix_version(self.args.version)
        else:
            exit_clowder_not_found()

    def forall(self):
        """clowder forall command"""
        if self.clowder is not None:
            cprint('Forall...\n', 'yellow')
            if self.args.groups is None:
                self.clowder.forall(self.args.cmd)
            else:
                self.clowder.forall_groups(self.args.cmd, self.args.groups)
        else:
            exit_clowder_not_found()

    def groom(self):
        """clowder groom command"""
        if self.clowder is not None:
            cprint('Groom...\n', 'yellow')
            self.clowder.groom()
        else:
            exit_clowder_not_found()

    def herd(self):
        """clowder herd command"""
        if self.clowder is not None:
            cprint('Herd...\n', 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.symlink_yaml(self.args.version)
            clowder = ClowderYAML(self.root_directory)
            if self.args.version is None:
                if self.args.groups is None:
                    clowder.herd_all()
                else:
                    clowder.herd_groups(self.args.groups)
            else:
                clowder.herd_version(self.args.version)
        else:
            exit_clowder_not_found()

    def meow(self):
        """clowder meow command"""
        if self.clowder is not None:
            cprint('Meow...\n', 'yellow')
            if self.args.verbose:
                self.clowder.meow_verbose()
            else:
                self.clowder.meow()
        else:
            exit_clowder_not_found()

    def stash(self):
        """clowder stash command"""
        if self.clowder is not None:
            cprint('Stash...\n', 'yellow')
            self.clowder.stash()
        else:
            exit_clowder_not_found()

    def sync(self):
        """clowder sync command"""
        if self.clowder is not None:
            cprint('Sync...\n', 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.sync()
        else:
            exit_clowder_not_found()

def main():
    """Main entrypoint for clowder command"""
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init()
    Command()

def exit_unrecognized_command(parser):
    """Print unrecognized command message and exit"""
    cprint('Unrecognized command\n', 'red')
    parser.print_help()
    print('')
    sys.exit(1)

def exit_clowder_not_found():
    """Print clowder not found message and exit"""
    print_clowder_not_found_message()
    sys.exit(1)

# Disable errors shown by pylint for unused arguments
# pylint: disable=W0613
def signal_handler(sig, frame):
    """Signal handler for Ctrl+C trap"""
    print('')
    sys.exit(0)
