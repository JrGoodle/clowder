"""Model representation of clowder.yaml group"""

from clowder.project import Project

class Group(object):
    """Model class for clowder.yaml group"""

    def __init__(self, rootDirectory, group, defaults, remotes):
        self.name = group['name']
        self.projects = []

        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, remotes))

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        projects_yaml = []

        for project in self.projects:
            projects_yaml.append(project.get_yaml())
        return {'name': self.name, 'projects': projects_yaml}
