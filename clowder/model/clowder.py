import os, sys

from project import Project

class Clowder(object):

    def __init__(self, path):
        self.path = path
        # self.defaultRemote = something
        # self.defaultRef = something
        # self.groups = currentGroups
        # self.remotes = remotes
        # self.projects = projects

    def getGroups(self):
        pass

    def getProjects(self):
        pass

class ProjectManager(object):

    def __init__(self, rootPath):
        projectList = os.path.join(rootPath, '.repo/project.list')
        self.projects = []
        with open(projectList) as file:
            for line in file:
                self.projects.append(Project(rootPath, line.strip()))

    def getProjectNames(self):
        projectNames = []
        for project in self.projects:
            projectNames.append(project.relativePath)
        return projectNames
