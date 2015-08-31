#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import os, signal, sys
import argcomplete, argparse
from termcolor import cprint
from clowder.model.clowder_repo import ClowderRepo
from clowder.model.clowder_yaml import ClowderYAML
from clowder.utility.clowder_utilities import (
    get_yaml_path,
    symlink_clowder_yaml
)
from clowder.utility.print_utilities import (
    print_clowder_not_found_message
)

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()
        # Load current clowder.yml config if it exists
        self.clowder = None
        groups = None
        versions = None
        if os.path.isdir(os.path.join(self.root_directory, 'clowder')):
            self.clowder = ClowderYAML(self.root_directory)
            versions = self.clowder.get_fixed_version_names()
            groups = self.clowder.get_all_group_names()

        # clowder argparse setup
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        subparsers = parser.add_subparsers(dest='command')
        # clowder breed
        parser_breed = subparsers.add_parser('breed',
                                             help=('Clone repository to clowder directory '
                                                   'and create clowder.yaml symlink'))
        parser_breed.add_argument('url', help='URL of repo containing clowder.yaml')
        # clowder herd
        parser_herd = subparsers.add_parser('herd',
                                            help='Clone and sync latest changes for projects')
        group = parser_herd.add_mutually_exclusive_group()
        group.add_argument('--version', '-v', choices=versions, help='Version name to herd')
        group.add_argument('--groups', '-g', choices=groups, nargs='+', help='Groups to herd')
        # clowder fix
        parser_fix = subparsers.add_parser('fix',
                                           help=('Create version of clowder.yaml'
                                                 ' for current repos'))
        parser_fix.add_argument('--version', '-v', required=True, help='Version name to fix')
        # clowder forall
        parser_forall = subparsers.add_parser('forall',
                                              help='Run command in all clowder projects')
        parser_forall.add_argument('cmd', help='Command to run in clowder projects')
        # clowder groom
        subparsers.add_parser('groom', add_help=False,
                              help='Update clowder repository with latest changes')
        # clowder litter
        subparsers.add_parser('litter', add_help=False,
                              help='Discard current changes in all projects and clowder repo')
        # clowder meow
        subparsers.add_parser('meow', add_help=False,
                              help='Print status for projects')
        # clowder stash
        subparsers.add_parser('stash', add_help=False,
                              help='Stash current changes in all projects and clowder repo')
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        print('')
        try:
            if not hasattr(self, self.args.command):
                cprint('Unrecognized command\n', 'red')
                parser.print_help()
                print('')
                exit(1)
        except:
            cprint('Unrecognized command\n', 'red')
            parser.print_help()
            print('')
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()
        print('')

    def breed(self):
        """clowder breed command"""
        if self.clowder == None:
            cprint('Breeding from %s\n' % self.args.url, 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.clone(self.args.url)
            yaml_file = os.path.join(self.root_directory, 'clowder/clowder.yaml')
            symlink_clowder_yaml(self.root_directory, yaml_file)
        else:
            cprint('Clowder already bred in this directory, exiting...\n', 'red')
            sys.exit()

    def fix(self):
        """clowder fix command"""
        if self.clowder != None:
            cprint('Fixing...\n', 'yellow')
            self.clowder.fix_version(self.args.version)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def forall(self):
        """clowder forall command"""
        if self.clowder != None:
            cprint('Forall...\n', 'yellow')
            self.clowder.forall(self.args.cmd)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def groom(self):
        """clowder groom command"""
        if self.clowder != None:
            cprint('Grooming...\n', 'yellow')
            clowder_repo = ClowderRepo(self.root_directory)
            clowder_repo.groom()
        else:
            print_clowder_not_found_message()
            sys.exit()

    def herd(self):
        """clowder herd command"""
        if self.clowder != None:
            cprint('Herding...\n', 'yellow')
            yaml_file = get_yaml_path(self.root_directory, self.args.version)
            symlink_clowder_yaml(self.root_directory, yaml_file)
            clowder = ClowderYAML(self.root_directory)
            if self.args.version == None:
                if self.args.groups == None:
                    clowder.herd_all()
                else:
                    clowder.herd_groups(self.args.groups)
            else:
                clowder.herd_version_all(self.args.version)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def litter(self):
        """clowder litter command"""
        if self.clowder != None:
            cprint('Litter...\n', 'yellow')
            self.clowder.litter()
        else:
            print_clowder_not_found_message()
            sys.exit()

    def meow(self):
        """clowder meow command"""
        if self.clowder != None:
            cprint('Meow...\n', 'yellow')
            self.clowder.meow()
        else:
            print_clowder_not_found_message()
            sys.exit()

    def stash(self):
        """clowder stash command"""
        if self.clowder != None:
            cprint('Stash...\n', 'yellow')
            self.clowder.stash()
        else:
            print_clowder_not_found_message()
            sys.exit()

def main():
    """Main entrypoint for clowder command"""
    signal.signal(signal.SIGINT, signal_handler)
    Command()

# Disable errors shown by pylint for unused arguments
# pylint: disable=W0613
def signal_handler(sig, frame):
    """Signal handler for Ctrl+C trap"""
    print('')
    sys.exit(0)
