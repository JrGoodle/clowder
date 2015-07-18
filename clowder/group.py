from clowder.project import Project

class Group(object):

    def __init__(self, name, projects):
        self.name = name
        self.projects = projects

    def syncProjects(self):
        pass

    def updateProjects(self):
        pass
