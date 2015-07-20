import os
import yaml

import git

from clowder.group import Group
from clowder.project import Project
from clowder.remote import Remote

import clowder.utilities

class ClowderController(object):

    def __init__(self, rootDirectory, clowderYAML):
        self.rootDirectory = rootDirectory
        self.clowderPath = os.path.join(self.rootDirectory, '.clowder')
        self.clowderRepo = self.getClowderRepo()

        self.parsedYAML = yaml.safe_load(clowderYAML)

        defaults = self.parsedYAML['defaults']
        self.defaultRef = defaults['ref']
        self.defaultRemote = defaults['remote']
        self.defaultGroups = defaults['groups']

        self.remotes = []
        self.initRemotes()

        self.allGroups = []
        self.initGroups()

    def initGroups(self):
        for group in self.parsedYAML['groups']:
            projects = []
            for project in group['projects']:
                projectName = project['name']
                path = project['path']

                if 'ref' in project:
                    ref = project['ref']
                else:
                    ref = self.defaultRef

                if 'remote' in project:
                    remoteName = project['remote']
                else:
                    remoteName = self.defaultRemote

                for remote in self.remotes:
                    if remote.name == remoteName:
                        projects.append(Project(self.rootDirectory, projectName, path, ref, remote))

            groupName = group['name']
            self.allGroups.append(Group(groupName, projects))

    def initRemotes(self):
        for remote in self.parsedYAML['remotes']:
            name = remote['name']
            url = remote['url']
            self.remotes.append(Remote(name, url))

    def getAllGroupNames(self):
        names = []
        for group in self.allGroups:
            names.append(group['name'])
        return names

    def getCurrentProjectNames(self):
        configFile = os.path.join(self.rootDirectory, '.clowder/config.yaml')
        if os.path.exists(configFile):
            with open(configFile) as file:
                yamlConfig = yaml.safe_load(file)
                return yamlConfig["currentProjectNames"]
        return None


    def getSnapshotNames(self):
        snapshotsDir = os.path.join(self.rootDirectory, '.clowder/snapshots')
        if os.path.exists(snapshotsDir):
            files = os.listdir(snapshotsDir)
            snapshots = []
            for name in files:
                snapshots.append(clowder.utilities.rchop(name, '.yaml'))
            return snapshots
        return None

    def getClowderRepo(self):
        repoDir = os.path.join(self.rootDirectory, '.clowder/repo')
        if os.path.isdir(os.path.join(repoDir, '.git')):
            return git.Repo(repoDir)
        return None

    def update(self):
        pass
