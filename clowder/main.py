#! /usr/bin/env python3

if __name__ == '__main__':
    import clowder
    raise SystemExit(main.main())

import argcomplete, argparse
import os, sys

import clowder.breed
import clowder.fix
import clowder.groom
import clowder.herd
import clowder.knead
import clowder.litter
import clowder.manifest
import clowder.meow
import clowder.play
import clowder.project
import clowder.projectManager
import clowder.purr
import clowder.nest

class Clowder(object):

    def __init__(self):
        self.rootDirectory = os.getcwd()
        self.clowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        self.manifest = clowder.manifest.Manifest(self.rootDirectory)
        self.projectManager = clowder.projectManager.ProjectManager(self.rootDirectory)

        parser = argparse.ArgumentParser(description='Manage multiple repositories')
        subparsers = parser.add_subparsers(dest='subparser_name', help='sub-command help')

        parser_breed = subparsers.add_parser('breed', help='breed help', description='Clone repositories')
        parser_breed.set_defaults(func=self.breed)
        parser_breed.add_argument('url') # TODO: save parameter and validate url
        parser_breed.add_argument('--groups', '-g', nargs='*', choices=self.manifest.getGroups())

        parser_herd = subparsers.add_parser('herd', help='herd help', description='Sync repositories')
        parser_herd.set_defaults(func=self.herd)
        versions = ['master']
        versions.extend(self.manifest.getVersions())
        parser_herd.add_argument('--version', '-v', choices=versions)
        parser_herd.add_argument('--groups', '-g', nargs='*', choices=self.manifest.getGroups())

        parser_play = subparsers.add_parser('play', help='play help', description='Create new topic branch(es)')
        parser_play.set_defaults(func=self.play)
        parser_play.add_argument('branch')
        parser_play.add_argument('projects', nargs='*', choices=self.projectManager.getProjectNames())

        parser_purr = subparsers.add_parser('purr', help='purr help', description='Commit and upload current peru.yaml')
        parser_purr.set_defaults(func=self.purr)

        parser_meow = subparsers.add_parser('meow', help='meow help', description='Print status of current repositories')
        parser_meow.set_defaults(func=self.meow)

        parser_knead = subparsers.add_parser('knead', help='knead help', description='Show diffs for current repositories')
        parser_knead.set_defaults(func=self.knead)

        parser_litter = subparsers.add_parser('litter', help='litter help', description='Discard local changes')
        parser_litter.set_defaults(func=self.litter)
        parser_litter.add_argument('projects', nargs='*', choices=self.projectManager.getProjectNames())

        parser_groom = subparsers.add_parser('groom', help='groom help', description='Prune obsolete remote branches')
        parser_groom.set_defaults(func=self.groom)

        parser_fix = subparsers.add_parser('fix', help='fix help', description='Save a version and tag it')
        parser_fix.set_defaults(func=self.fix)
        parser_fix.add_argument('version')

        parser_nest = subparsers.add_parser('nest', help='nest help')
        parser_nest.set_defaults(func=self.nest)

        argcomplete.autocomplete(parser)
        self.args = parser.parse_args()

    def breed(self):
        if os.path.exists(self.clowderDirectory):
            print('Clowder already bred in this directory, exiting...')
            sys.exit()
        else:
            print('Breeding clowder...')
        print('Running clowder breed, url=%s' % self.args.url)
        clowder.breed.Breed(self.rootDirectory, self.args.url, self.args.groups)

    def herd(self):
        self.checkClowderDirectory()
        print('Running clowder herd, version=%s' % self.args.version)
        clowder.herd.Herd(self.rootDirectory, self.args.version, self.args.groups)

    def play(self):
        self.checkClowderDirectory()
        print('Running clowder play, branch=%s' % self.args.branch)
        clowder.play.Play(self.args.branch, self.args.projects)

    def purr(self):
        self.checkClowderDirectory()
        print('Running clowder purr')
        clowder.purr.Purr(self.rootDirectory)

    def meow(self):
        self.checkClowderDirectory()
        print('Running clowder meow')
        clowder.meow.Meow()

    def knead(self):
        self.checkClowderDirectory()
        print('Running clowder knead')
        clowder.knead.Knead()

    def litter(self):
        self.checkClowderDirectory()
        print('Running clowder litter')
        clowder.litter.Litter(self.args.projects)

    def groom(self):
        self.checkClowderDirectory()
        print('Running clowder groom')
        clowder.groom.Groom()

    def fix(self):
        self.checkClowderDirectory()
        print('Running clowder fix, version=%s' % self.args.version)
        clowder.fix.Fix(self.args.version)

    def nest(self):
        print('Running clowder nest')
        clowder.nest.Nest()

    def checkClowderDirectory(self):
        if not os.path.exists(self.clowderDirectory):
            print("Clowder doesn't seem to exist in this directory")
            sys.exit()

def main():
    Clowder()
