#! /usr/bin/env python3

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse
import os, sys

from clowder.breed import breed
from clowder.herd import herd
from clowder.meow import meow
from clowder.clowderController import ClowderController

class Command(object):

    def __init__(self):
        self.rootDirectory = os.getcwd()

        # Set argument
        self.clowder = None
        self.allGroupNames = []
        self.currentProjectNames = []

        yamlFile = os.path.join(self.rootDirectory, 'clowder.yaml')
        if os.path.exists(yamlFile):
            with open(yamlFile) as file:
                self.clowder = ClowderController(self.rootDirectory, file)
                # self.allGroupNames = self.clowder.getAllGroupNames()
                # self.currentProjectNames = self.clowder.getCurrentProjectNames()

        # clowder argparse setup
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        self.subparsers = parser.add_subparsers(dest='command', help='clowder command help')

        parser_breed = self.subparsers.add_parser('breed', help='breed help', description='Clone repositories')
        parser_breed.add_argument('url')

        parser_herd = self.subparsers.add_parser('herd', help='herd help', description='Sync repositories')

        parser_meow = self.subparsers.add_parser('meow', help='meow help', description='Repository Status')

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
            print('Breeding the cats..., url=%s\n' % self.args.url)
            breed(self.rootDirectory, self.args.url)
        else:
            print('Clowder already bred in this directory, exiting...')
            sys.exit()

    def herd(self):
        if self.clowder != None:
            print('Herding the cats...\n')
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
