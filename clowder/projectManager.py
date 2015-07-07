import os

import clowder.project

class ProjectManager(object):

    def __init__(self, rootPath):
        projectList = os.path.join(rootPath, '.repo/project.list')
        self.projects = []
        with open(projectList) as file:
            for line in file:
                self.projects.append(clowder.project.Project(rootPath, line.strip()))

    def getProjectNames(self):
        projectNames = []
        for project in self.projects:
            projectNames.append(project.relativePath)
        return projectNames
