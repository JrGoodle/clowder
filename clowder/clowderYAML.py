"""clowder.yaml parsing and functionality"""
import os
import yaml

from clowder.defaults import Defaults
from clowder.group import Group
from clowder.remote import Remote

class ClowderYAML(object):
    def __init__(self, rootDirectory):
        self.rootDirectory = rootDirectory

        self.defaults = None
        self.groups = []
        self.remotes = []

        yamlFile = os.path.join(self.rootDirectory, 'clowder.yaml')
        if os.path.exists(yamlFile):
            with open(yamlFile) as file:
                parsedYAML = yaml.safe_load(file)

                self.defaults = Defaults(parsedYAML['defaults'])

                for remote in parsedYAML['remotes']:
                    self.remotes.append(Remote(remote))

                for group in parsedYAML['groups']:
                    self.groups.append(Group(self.rootDirectory,
                                             group,
                                             self.defaults,
                                             self.remotes))

    def getAllGroupNames(self):
        names = []
        for group in self.groups:
            names.append(group['name'])
        return names

    def sync(self):
        for group in self.groups:
            for project in group.projects:
                project.sync()

    def syncVersion(self, version):
        for group in self.groups:
            for project in group.projects:
                project.syncVersion(version)

    def status(self):
        for group in self.groups:
            for project in group.projects:
                project.status()

    def fixVersion(self, version):
        versionsPath = os.path.join(self.rootDirectory, 'clowder/versions')
        versionDirectory = os.path.join(versionsPath, version)
        if not os.path.exists(versionDirectory):
            os.makedirs(versionDirectory)

        yamlFile = os.path.join(versionDirectory, 'clowder.yaml')
        if not os.path.exists(yamlFile):
            with open(yamlFile, 'w') as file:
                yaml.dump(self.getYAML(), file, default_flow_style=False)

    def getYAML(self):
        groupsYAML = []
        for group in self.groups:
            groupsYAML.append(group.getYAML())

        remotesYAML = []
        for remote in self.remotes:
            remotesYAML.append(remote.getYAML())

        return {'defaults': self.defaults.getYAML(),
                'remotes': remotesYAML,
                'groups': groupsYAML}
