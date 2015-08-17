import os
import sh, yaml

from clowder.project import Project

class Group(object):
    def __init__(self, rootDirectory, group, defaults, remotes):
        self.name = group['name']
        self.projects = []

        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, remotes))

    def getYAML(self):
        projectsYAML = []

        for project in self.projects:
            projectsYAML.append(project.getYAML())
        return {'name': self.name, 'projects': projectsYAML}
