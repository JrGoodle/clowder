#! /usr/bin/env python3

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse
import os, sys

from clowder.subcommands import breed, herd, meow, groom, fix
from clowder.clowderYAML import ClowderYAML

class Command(object):

    def __init__(self):
        self.rootDirectory = os.getcwd()

        # Set argument
        self.clowder = None
        self.allGroupNames = []
        self.currentProjectNames = []

        if os.path.isdir(os.path.join(self.rootDirectory, '.clowder')):
            self.clowder = ClowderYAML(self.rootDirectory)

        # clowder argparse setup
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        self.subparsers = parser.add_subparsers(dest='command', help='clowder command help')

        parser_breed = self.subparsers.add_parser('breed', help='breed help', description='Clone repositories')
        parser_breed.add_argument('url')

        parser_groom = self.subparsers.add_parser('groom', help='groom help', description='Sync clowder repository')

        parser_herd = self.subparsers.add_parser('herd', help='herd help', description='Sync project repositories')

        parser_meow = self.subparsers.add_parser('meow', help='meow help', description='Repository Status')

        parser_fix = self.subparsers.add_parser('fix', help='fix help', description='Update clowder.yaml')
        parser_fix.add_argument('--version', '-v')

        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        if not hasattr(self, self.args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()

    def breed(self):
        if self.clowder == None:
            print('Breeding from %s\n' % self.args.url)
            breed(self.rootDirectory, self.args.url)
        else:
            print('Clowder already bred in this directory, exiting...')
            sys.exit()

    def fix(self):
        if self.clowder != None:
            print('Fixing...\n')
            fix(self.rootDirectory, self.args.version)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def groom(self):
        if self.clowder != None:
            print('Grooming...\n')
            groom(self.rootDirectory)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def herd(self):
        if self.clowder != None:
            print('Herding...\n')
            herd(self.rootDirectory)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def meow(self):
        if self.clowder != None:
            print('Meow...\n')
            meow(self.rootDirectory)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

def main():
    Command()
