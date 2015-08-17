import os
import sh, yaml

from clowder.defaults import Defaults
from clowder.group import Group
from clowder.project import Project
from clowder.remote import Remote

class ClowderYAML(object):
    def __init__(self, rootDirectory):
        self.rootDirectory = rootDirectory

        self.defaults = None
        self.groups = []
        self.remotes = []

        yamlFile = os.path.join(rootDirectory, 'clowder.yaml')
        if os.path.exists(yamlFile):
            with open(yamlFile) as file:
                parsedYAML = yaml.safe_load(file)

                self.defaults = Defaults(parsedYAML['defaults'])

                for remote in parsedYAML['remotes']:
                    self.remotes.append(Remote(remote))

                for group in parsedYAML['groups']:
                    self.groups.append(Group(self.rootDirectory, group, self.defaults, self.remotes))

    def getAllGroupNames(self):
        names = []
        for group in self.groups:
            names.append(group['name'])
        return names

    def sync(self):
        for group in self.groups:
            for project in group.projects:
                project.sync()

    def status(self):
        for group in self.groups:
            for project in group.projects:
                project.status()

    def fixVersion(self, version):
        versionsDirectory = os.path.join(self.rootDirectory, '.clowder/repo/versions')
        if not os.path.exists(versionsDirectory):
            os.mkdir(versionsDirectory)

        yamlFile = os.path.join(versionsDirectory, version + '.yaml')
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

def process_output(line):
    print(line)
