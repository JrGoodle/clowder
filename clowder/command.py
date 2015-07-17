#! /usr/bin/env python3

if __name__ == '__main__':
    raise SystemExit(main())

import argcomplete, argparse
import os, sys

from clowder.commands.breed import Breed
from clowder.commands.fix import Fix
from clowder.commands.groom import Groom
from clowder.commands.herd import Herd
from clowder.commands.knead import Knead
from clowder.commands.litter import Litter
from clowder.commands.meow import Meow
from clowder.commands.play import Play
from clowder.commands.purr import Purr
from clowder.commands.nest import Nest

from clowder.model.parser import Parser
from clowder.model.clowder import Clowder

class Command(object):

    def __init__(self):
        self.rootDirectory = os.getcwd()
        self.clowderPath = os.path.join(self.rootDirectory, '.clowder')

        if os.path.exists(self.clowderPath):
            self.yamlParser = Parser(self.rootDirectory)
            self.clowder = Clowder(self.yamlParser)
            allGroups = self.yamlParser.getGroups()
            currentProjects = self.clowder.getProjects()
            snapshots = self.yamlParser.getSnapshots()
        else:
            self.yamlParser = None
            self.clowder = None
            allGroups = []
            currentProjects = []
            snapshots = []

        # clowder
        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        subparsers = parser.add_subparsers(dest='command', help='sub-command help')

        # clowder breed
        parser_breed = subparsers.add_parser('breed', help='breed help', description='Clone repositories')
        parser_breed.add_argument('url')
        parser_breed.add_argument('--groups', '-g', nargs='+', choices=allGroups)

        # clowder herd
        parser_herd = subparsers.add_parser('herd', help='herd help', description='Sync repositories')
        versions = ['master']
        versions.extend(snapshots)
        parser_herd.add_argument('--version', '-v', choices=versions)
        parser_herd.add_argument('--groups', '-g', nargs='+', choices=allGroups)

        # clowder play
        parser_play = subparsers.add_parser('play', help='play help', description='Create new topic branch(es)')
        parser_play.add_argument('branch')
        parser_play.add_argument('projects', nargs='+', choices=currentProjects)

        # clowder purr
        subparsers.add_parser('purr', help='purr help', description='Commit and upload current peru.yaml')

        # clowder meow
        subparsers.add_parser('meow', help='meow help', description='Print status of current repositories')

        # clowder knead
        subparsers.add_parser('knead', help='knead help', description='Show diffs for current repositories')

        # clowder litter
        parser_litter = subparsers.add_parser('litter', help='litter help', description='Discard local changes')
        parser_litter.add_argument('projects', nargs='*', choices=currentProjects)

        # clowder groom
        subparsers.add_parser('groom', help='groom help', description='Prune obsolete remote branches')

        # clowder fix
        parser_fix = subparsers.add_parser('fix', help='fix help', description='Save a version and tag it')
        parser_fix.add_argument('version')

        # clowder nest
        subparsers.add_parser('nest', help='nest help')

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
            print('Breeding clowder...')
            print('Running clowder breed, url=%s' % self.args.url)
            Breed(self.rootDirectory, self.args.url, self.args.groups)
        else:
            print('Clowder already bred in this directory, exiting...')
            sys.exit()

    def herd(self):
        if self.clowder != None:
            print('Running clowder herd, version=%s' % self.args.version)
            Herd(self.rootDirectory, self.args.version, self.args.groups)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def play(self):
        if self.clowder != None:
            print('Running clowder play, branch=%s' % self.args.branch)
            Play(self.args.branch, self.args.projects)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def purr(self):
        if self.clowder != None:
            print('Running clowder purr')
            Purr(self.rootDirectory)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def meow(self):
        if self.clowder != None:
            print('Running clowder meow')
            Meow()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def knead(self):
        if self.clowder != None:
            print('Running clowder knead')
            Knead()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def litter(self):
        if self.clowder != None:
            print('Running clowder litter')
            Litter(self.args.projects)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def groom(self):
        if self.clowder != None:
            print('Running clowder groom')
            Groom()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def fix(self):
        if self.clowder != None:
            print('Running clowder fix, version=%s' % self.args.version)
            Fix(self.args.version)
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

    def nest(self):
        if self.clowder != None:
            print('Running clowder nest')
            Nest()
        else:
            print('No .clowder found in the current directory, exiting...')
            sys.exit()

def main():
    Command()
