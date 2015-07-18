#! /usr/bin/env python3

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse
import os, sys

from clowder.commands.breed import Breed
from clowder.commands.fix import Fix
from clowder.commands.herd import Herd
from clowder.commands.knead import Knead
from clowder.commands.meow import Meow
from clowder.commands.play import Play

from clowder.model.clowder import Clowder

class Command(object):

    def __init__(self):
        self.rootDirectory = os.getcwd()
        self.clowderPath = os.path.join(self.rootDirectory, '.clowder')

        self.yamlParser = None
        self.clowder = None
        self.allGroupNames = []
        self.currentProjectNames = []
        self.snapshotNames = []

        if os.path.exists(self.clowderPath):
            with open(self.clowderPath) as file:
                self.clowder = Clowder(file)
                self.allGroupNames = self.clowder.getAllGroupNames()
                self.currentProjectNames = self.clowder.getCurrentProjectNames()
                self.snapshotNames = self.clowder.getSnapshotNames()

        # clowder argparse setup
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        self.subparsers = parser.add_subparsers(dest='command', help='clowder command help')
        self.setupSubparsers()
        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

        if not hasattr(self, self.args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, self.args.command)()

    def breedParser(self):
        parser_breed = self.subparsers.add_parser('breed', help='breed help', description='Clone repositories')
        parser_breed.add_argument('url')

    def breed(self):
        if self.clowder == None:
            print('Breeding clowder...')
            print('Running clowder breed, url=%s' % self.args.url)
            Breed(self.rootDirectory, self.args.url)
        else:
            print('Clowder already bred in this directory, exiting...')
            sys.exit()

    def herdParser(self):
        parser_herd = self.subparsers.add_parser('herd', help='herd help', description='Sync repositories')
        versions = ['master']
        versions.extend(self.snapshotNames)
        parser_herd.add_argument('--version', '-v', choices=versions)
        parser_herd.add_argument('--groups', '-g', nargs='+', choices=self.allGroupNames)

    def herd(self):
        if self.clowder != None:
            print('Running clowder herd, version=%s' % self.args.version)
            Herd(self.rootDirectory, self.args.version, self.args.groups)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def playParser(self):
        parser_play = self.subparsers.add_parser('play', help='play help', description='Create new topic branch(es)')
        parser_play.add_argument('branch')
        parser_play.add_argument('projects', nargs='+', choices=self.currentProjectNames)

    def play(self):
        if self.clowder != None:
            print('Running clowder play, branch=%s' % self.args.branch)
            Play(self.args.branch, self.args.projects)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def meowParser(self):
        self.subparsers.add_parser('meow', help='meow help', description='Print status of current repositories')

    def meow(self):
        if self.clowder != None:
            print('Running clowder meow')
            Meow()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def kneadParser(self):
        self.subparsers.add_parser('knead', help='knead help', description='Show diffs for current repositories')

    def knead(self):
        if self.clowder != None:
            print('Running clowder knead')
            Knead()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def fixParser(self):
        parser_fix = self.subparsers.add_parser('fix', help='fix help', description='Save a version and tag it')
        parser_fix.add_argument('version')

    def fix(self):
        if self.clowder != None:
            print('Running clowder fix, version=%s' % self.args.version)
            Fix(self.args.version)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def setupSubparsers(self):
        self.breedParser()
        self.fixParser()
        self.herdParser()
        self.kneadParser()
        self.meowParser()
        self.playParser()

def main():
    Command()
