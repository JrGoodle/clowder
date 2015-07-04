#! /usr/bin/env python3

import argparse
import sys
import os

import clowder.breed
import clowder.fix
import clowder.groom
import clowder.herd
import clowder.knead
import clowder.litter
import clowder.meow
import clowder.play
import clowder.project
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
  purr       Push new commits to remote branch(es)
  meow       Print status of current repositories
  knead      Show diffs for current repositories

Utilities:
  litter     Discard local changes
  groom      Prune obsolete remote branches
  fix        Save a version and tag it
  nest       Delete directory contents for breeding

''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        self.rootDirectory = os.getcwd()
        self.clowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        print(self.clowderDirectory)
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
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder breed, url=%s' % args.url)
        clowder.breed.Breed(args.url, self.clowderDirectory)

    def herd(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Sync repositories')
        parser.add_argument('--version', '-v')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder herd, version=%s' % args.version)
        clowder.herd.Herd(args.version)

    def play(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Create new topic branch(es)')
        parser.add_argument('branch')
        parser.add_argument('projects', nargs='*', choices=self.getProjectNames())
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder play, branch=%s' % args.branch)
        clowder.play.Play(args.branch, args.projects)

    # def purr(self):
    #     self.checkClowderDirectory()
    #     parser = argparse.ArgumentParser(
    #         description='Push new commits to remote branch(es)')
    #     args = parser.parse_args(sys.argv[2:])
    #     print('Running clowder purr')
    #     clowder.purr.Purr()

    def meow(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Print status of current repositories')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder meow')
        clowder.meow.Meow()

    def knead(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Show diffs for current repositories')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder knead')
        clowder.knead.Knead()

    def litter(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Discard local changes')
        # parser.add_argument('project') # TODO: perform action for all projects
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder litter')# , project=%s' % args.project)
        clowder.litter.Litter()

    def groom(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Prune obsolete remote branches')
        args = parser.parse_args(sys.argv[2:])
        print('Running clowder groom')
        clowder.groom.Groom()

    def fix(self):
        self.checkClowderDirectory()
        parser = argparse.ArgumentParser(
            description='Save a version and tag it')
        parser.add_argument('version')
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

    def getProjects(self):
        projectList = os.path.join(self.rootDirectory, '.repo/project.list')
        # if os.path.isfile(projectList)
        projects = []
        with open(projectList) as file:
            for line in file:
                projects.append(clowder.project.Project(self.rootDirectory, line))
        for project in projects:
            print('Project name: ' + project.name)
        return projects

    def getProjectNames(self):
        projectNames = []
        for project in self.getProjects():
            projectNames.append(project.relativePath)
        return projectNames

if __name__ == '__main__':
    Clowder()
