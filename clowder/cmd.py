#! /usr/bin/env python3
"""Main entrypoint for clowder command"""

if __name__ == '__main__':
    raise SystemExit(main())

import os, sys

import argcomplete, argparse
from termcolor import cprint

from clowder.subcommands import breed, herd, meow, groom, fix, litter
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
        self.subparsers = parser.add_subparsers(dest='command',
                                                help='clowder command help')
        # clowder breed
        parser_breed = self.subparsers.add_parser('breed',
                                                  help='breed help',
                                                  description='Clone repositories')
        parser_breed.add_argument('url')
        # clowder groom
        self.subparsers.add_parser('groom',
                                   help='groom help',
                                   description='Sync clowder repository')
        # clowder herd
        parser_herd = self.subparsers.add_parser('herd',
                                                 help='herd help',
                                                 description='Sync project repositories')
        parser_herd.add_argument('--version', '-v', choices=versions)

        # clowder meow
        self.subparsers.add_parser('meow',
                                   help='meow help',
                                   description='Repository Status')
        # clowder fix
        parser_fix = self.subparsers.add_parser('fix',
                                                help='fix help',
                                                description='Update clowder.yaml')
        parser_fix.add_argument('--version', '-v', required=True)
        # clowder litter
        self.subparsers.add_parser('litter',
                                   help='litter help',
                                   description='Discard current changes')
        # Argcomplete and arguments parsing
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        if not hasattr(self, self.args.command):
            cprint('Unrecognized command', 'red')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()

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
            cprint('No .clowder found in the current directory, exiting...\n', 'red')
            sys.exit()

    def groom(self):
        """clowder groom command"""
        if self.clowder != None:
            cprint('Grooming...\n', 'yellow')
            groom(self.root_directory)
        else:
            cprint('No .clowder found in the current directory, exiting...\n', 'red')
            sys.exit()

    def herd(self):
        """clowder herd command"""
        if self.clowder != None:
            cprint('Herding...\n', 'yellow')
            herd(self.root_directory, self.args.version)
        else:
            cprint('No .clowder found in the current directory, exiting...\n', 'red')
            sys.exit()

    def litter(self):
        """clowder litter command"""
        if self.clowder != None:
            cprint('Litter...\n', 'yellow')
            litter(self.root_directory)
        else:
            cprint('No .clowder found in the current directory, exiting...\n', 'red')
            sys.exit()

    def meow(self):
        """clowder meow command"""
        if self.clowder != None:
            cprint('Meow...\n', 'yellow')
            meow(self.root_directory)
        else:
            cprint('No .clowder found in the current directory, exiting...\n', 'red')
            sys.exit()

def main():
    """Main entrypoint for clowder command"""
    Command()
