import yaml

from group import Group
from project import Project
from remote import Remote

class Clowder(object):

    def __init__(self, file):
        self.parsedYAML = yaml.safe_load(file)

        defaults = self.parsedYAML['defaults']
        self.defaultRef = defaults['ref']
        self.defaultRemote = defaults['remote']
        self.defaultGroups = defaults['groups']

        self.allGroups = []
        self.initGroups()

        self.remotes = []
        self.initRemotes()

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
                    remote = project['remote']
                else:
                    ref = self.defaultRemote

                projects.append(Project(projectName, path, ref, remote))

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
        # TODO: Read from file saved to disk
        pass

    def getSnapshotNames(self):
        # TODO: Read from file saved to disk
        pass
