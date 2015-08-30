#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import os, sys
import argcomplete, argparse
from termcolor import cprint
from clowder.subcommands import breed, herd, meow, groom, fix, forall, litter
from clowder.model.clowder_yaml import ClowderYAML

class Command(object):
    """Command class for parsing commandline options"""

    def __init__(self):
        self.root_directory = os.getcwd()

        # Load current clowder.yml config if it exists
        self.clowder = None
        versions = None
        if os.path.isdir(os.path.join(self.root_directory, 'clowder')):
            self.clowder = ClowderYAML(self.root_directory)
            versions = self.clowder.get_fixed_version_names()

        # clowder argparse setup
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        self.subparsers = parser.add_subparsers(dest='command')
        # clowder breed
        parser_breed = self.subparsers.add_parser('breed',
                                                  help=('Clone repository to clowder directory '
                                                        'and create clowder.yaml symlink'))
        parser_breed.add_argument('url', help='URL to clone repo with clowder.yaml from')
        # clowder forall
        parser_forall = self.subparsers.add_parser('forall',
                                                   help='Run command in all clowder projects')
        parser_forall.add_argument('run_command', help='Command to run in clowder projects')
        # clowder groom
        self.subparsers.add_parser('groom',
                                   help='Update clowder repository with latest changes')
        # clowder herd
        parser_herd = self.subparsers.add_parser('herd',
                                                 help='Clone and sync latest changes for projects')
        parser_herd.add_argument('--version', '-v', choices=versions, help='Version name to herd')
        # clowder meow
        self.subparsers.add_parser('meow',
                                   help='Print status for projects')
        # clowder fix
        parser_fix = self.subparsers.add_parser('fix',
                                                help=('Create version of clowder.yaml'
                                                      ' for current repos'))
        parser_fix.add_argument('--version', '-v', required=True, help='Version name to fix')
        # clowder litter
        self.subparsers.add_parser('litter',
                                   help='Discard current changes in all projects and clowder repo')
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        try:
            if not hasattr(self, self.args.command):
                cprint('\nUnrecognized command\n', 'red')
                parser.print_help()
                print('')
                exit(1)
        except:
            cprint('\nUnrecognized command\n', 'red')
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
            breed(self.root_directory, self.args.url)
        else:
            cprint('Clowder already bred in this directory, exiting...\n', 'red')
            sys.exit()

    def fix(self):
        """clowder fix command"""
        if self.clowder != None:
            cprint('Fixing...\n', 'yellow')
            fix(self.root_directory, self.args.version)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def forall(self):
        """clowder forall command"""
        if self.clowder != None:
            cprint('Forall...\n', 'yellow')
            forall(self.root_directory, self.args.run_command)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def groom(self):
        """clowder groom command"""
        if self.clowder != None:
            cprint('Grooming...\n', 'yellow')
            groom(self.root_directory)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def herd(self):
        """clowder herd command"""
        if self.clowder != None:
            cprint('Herding...\n', 'yellow')
            herd(self.root_directory, self.args.version)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def litter(self):
        """clowder litter command"""
        if self.clowder != None:
            cprint('Litter...\n', 'yellow')
            litter(self.root_directory)
        else:
            print_clowder_not_found_message()
            sys.exit()

    def meow(self):
        """clowder meow command"""
        if self.clowder != None:
            cprint('Meow...\n', 'yellow')
            meow(self.root_directory)
        else:
            print_clowder_not_found_message()
            sys.exit()

def print_clowder_not_found_message():
    """Print error message when clowder not found"""
    cprint('No clowder found in the current directory, exiting...\n', 'red')

def main():
    """Main entrypoint for clowder command"""
    Command()
