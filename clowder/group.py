from clowder.project import Project

class Group(object):

    def __init__(self, name, projects):
        self.name = name
        self.projects = projects

    def sync(self):
        for project in self.projects:
            project.sync()

    def status(self):
        for project in self.projects:
            project.status()
