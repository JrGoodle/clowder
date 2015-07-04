#! /usr/bin/env python3

import argparse
import sys

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
  purr       Push new commits to remote branch(es)
  meow       Print status of current repositories
  knead      Show diffs for current repositories

Utilities:
  litter     Discard local changes
  groom      Prune obsolete remote branches
  fix        Save a version and tag it
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def breed(self):
        parser = argparse.ArgumentParser(
            description='Clone repositories')
        parser.add_argument('url') # TODO: save parameter and validate url
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder breed, url=%s' % args.url)

    def herd(self):
        parser = argparse.ArgumentParser(
            description='Sync repositories')
        parser.add_argument('--version')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder herd, version=%s' % args.version)

    def play(self):
        parser = argparse.ArgumentParser(
            description='Create new topic branch(es)')
        parser.add_argument('branch')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder play, branch=%s' % args.branch)

    def purr(self):
        parser = argparse.ArgumentParser(
            description='Push new commits to remote branch(es)')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder purr')

    def meow(self):
        parser = argparse.ArgumentParser(
            description='Print status of current repositories')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder meow')

    def knead(self):
        parser = argparse.ArgumentParser(
            description='Show diffs for current repositories')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder knead')

    def litter(self):
        parser = argparse.ArgumentParser(
            description='Discard local changes')
        parser.add_argument('project') # TODO: perform action for all projects
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder litter, project=%s' % args.project)

    def groom(self):
        parser = argparse.ArgumentParser(
            description='Prune obsolete remote branches')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder groom')

    def fix(self):
        parser = argparse.ArgumentParser(
            description='Save a version and tag it')
        parser.add_argument('version')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder fix, version=%s' % args.version)

if __name__ == '__main__':
    Clowder()
