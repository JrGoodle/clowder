#! /usr/bin/env python3

if __name__ == '__main__':
    import clowder
    raise SystemExit(clowder.main())

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
        parser = argparse.ArgumentParser(
            description='Manage multiple repositories',
            usage='''clowder <command> [<args>]

Syncing:
  breed      Clone repositories
  herd       Sync repositories

Working:
  play       Create new topic branch(es)
  purr       Commit and upload current peru.yaml
  meow       Print status of current repositories
  knead      Show diffs for current repositories

Utilities:
  litter     Discard local changes
  groom      Prune obsolete remote branches
  fix        Save a version and tag it
  nest       Delete directory contents for breeding

''')
        commands = ['breed', 'herd']
        commands.extend(['play', 'purr', 'meow', 'knead'])
        commands.extend(['litter', 'groom', 'fix', 'nest'])
        parser.add_argument('command', help='Subcommand to run', choices=commands)
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        self.rootDirectory = os.getcwd()
        self.clowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def breed(self):
        if os.path.exists(self.clowderDirectory):
            print('Clowder already bred in this directory, exiting...')
            sys.exit()
        else:
            print('Breeding clowder...')
        parser = argparse.ArgumentParser(
            description='Clone repositories')
        parser.add_argument('url') # TODO: save parameter and validate url
        manifest = clowder.manifest.Manifest(self.rootDirectory)
        parser.add_argument('--groups', '-g', nargs='*', choices=manifest.getGroups())
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder breed, url=%s' % args.url)
        clowder.breed.Breed(self.rootDirectory, args.url, args.groups)

    def herd(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Sync repositories')
        manifest = clowder.manifest.Manifest(self.rootDirectory)
        versions = ['master']
        versions.extend(manifest.getVersions())
        parser.add_argument('--version', '-v', choices=versions)
        parser.add_argument('--groups', '-g', nargs='*', choices=manifest.getGroups())
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder herd, version=%s' % args.version)
        clowder.herd.Herd(self.rootDirectory, args.version, args.groups)

    def play(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Create new topic branch(es)')
        parser.add_argument('branch')
        projectManager = clowder.projectManager.ProjectManager(self.rootDirectory)
        parser.add_argument('projects', nargs='*', choices=projectManager.getProjectNames())
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder play, branch=%s' % args.branch)
        clowder.play.Play(args.branch, args.projects)

    def purr(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Commit and upload current peru.yaml')
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder purr')
        clowder.purr.Purr(self.rootDirectory)

    def meow(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Print status of current repositories')
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder meow')
        clowder.meow.Meow()

    def knead(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Show diffs for current repositories')
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder knead')
        clowder.knead.Knead()

    def litter(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Discard local changes')
        projectManager = clowder.projectManager.ProjectManager(self.rootDirectory)
        parser.add_argument('projects', nargs='*', choices=projectManager.getProjectNames())
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder litter')
        clowder.litter.Litter(args.projects)

    def groom(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Prune obsolete remote branches')
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder groom')
        clowder.groom.Groom()

    def fix(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Save a version and tag it')
        parser.add_argument('version')
        argcomplete.autocomplete(parser)
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder fix, version=%s' % args.version)
        clowder.fix.Fix(args.version)

    def nest(self):
        print('Running clowder nest')
        clowder.nest.Nest()

    def checkClowderDirectory(self):
        if not os.path.exists(self.clowderDirectory):
            print("Clowder doesn't seem to exist in this directory")
            sys.exit()

def main():
    Clowder()
