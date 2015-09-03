"""Model representation of clowder.yaml group"""

from clowder.model.project import Project
from clowder.utility.print_utilities import print_group

class Group(object):
    """Model class for clowder.yaml group"""

    def __init__(self, rootDirectory, group, defaults, sources):
        self.name = group['name']
        self.projects = []
        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, sources))
        self.projects.sort(key=lambda project: project.path)

    def get_all_project_names(self):
        """Return all project names"""
        project_names = []
        for project in self.projects:
            project_names.append(project.name)
        return project_names

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        projects_yaml = []
        for project in self.projects:
            projects_yaml.append(project.get_yaml())
        return {'name': self.name, 'projects': projects_yaml}

    def groom(self):
        """Discard changes for all projects"""
        if self.is_dirty():
            self._print_name()
            for project in self.projects:
                project.groom()

    def herd(self):
        """Sync all projects with latest upstream changes"""
        self._print_name()
        for project in self.projects:
            project.herd()

    def herd_version(self, version):
        """Sync all projects to fixed versions"""
        self._print_name()
        for project in self.projects:
            project.herd_version(version)

    def is_dirty(self):
        """Check if group has dirty project(s)"""
        is_dirty = False
        for project in self.projects:
            if project.is_dirty():
                is_dirty = True
        return is_dirty

    def meow(self):
        """Print status for all projects"""
        self._print_name()
        for project in self.projects:
            project.meow()

    def meow_verbose(self):
        """Print verbose status for all projects"""
        self._print_name()
        for project in self.projects:
            project.meow_verbose()

    def stash(self):
        """Stash changes for all projects with changes"""
        if self.is_dirty():
            self._print_name()
            for project in self.projects:
                project.stash()

    def is_valid(self):
        """Validate status of all projects"""
        valid = True
        for project in self.projects:
            if not project.is_valid():
                valid = False
        return valid

    def _print_name(self):
        """Print formatted group name"""
        print_group(self.name)

    def print_validation(self):
        """Print validation message for projects in group"""
        if not self.is_valid():
            self._print_name()
            for project in self.projects:
                project.print_validation()
