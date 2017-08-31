"""Representation of clowder.yaml group"""
from termcolor import colored
from clowder.project import Project

class Group(object):
    """clowder.yaml group class"""

    def __init__(self, rootDirectory, group, defaults, sources):
        self.name = group['name']
        self.projects = []
        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, sources))
        self.projects.sort(key=lambda project: project.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        projects_yaml = [p.get_yaml() for p in self.projects]
        return {'name': self.name, 'projects': projects_yaml}

    def clean(self):
        """Discard changes for all projects"""
        if self.is_dirty():
            self._print_name()
            for project in self.projects:
                project.clean()

    def fetch(self):
        """Silently fetch changes for all projects"""
        for project in self.projects:
            project.fetch()

    def herd(self, branch=None, depth=None):
        """Sync all projects with latest upstream changes"""
        self._print_name()
        for project in self.projects:
            project.herd(branch, depth)

    def is_dirty(self):
        """Check if group has dirty project(s)"""
        is_dirty = False
        for project in self.projects:
            if project.is_dirty():
                is_dirty = True
        return is_dirty

    def is_valid(self):
        """Validate status of all projects"""
        valid = True
        for project in self.projects:
            if not project.is_valid():
                valid = False
        return valid

    def print_existence_message(self):
        """Print existence validation message for projects in group"""
        if not self.projects_exist():
            self._print_name()
            for project in self.projects:
                project.print_exists()

    def print_validation(self):
        """Print validation message for projects in group"""
        if not self.is_valid():
            self._print_name()
            for project in self.projects:
                project.print_validation()

    def projects_exist(self):
        """Validate existence status of all projects"""
        projects_exist = True
        for project in self.projects:
            if not project.exists():
                projects_exist = False
        return projects_exist

    def prune(self, branch, is_remote, force):
        """Prune branch"""
        self._print_name()
        for project in self.projects:
            project.prune(branch, is_remote, force)

    def start(self, branch):
        """Start a new feature branch"""
        self._print_name()
        for project in self.projects:
            project.start(branch)

    def status(self):
        """Print status for all projects"""
        self._print_name()
        for project in self.projects:
            project.status()

    def status_verbose(self):
        """Print verbose status for all projects"""
        self._print_name()
        for project in self.projects:
            project.status_verbose()

    def stash(self):
        """Stash changes for all projects with changes"""
        if self.is_dirty():
            self._print_name()
            for project in self.projects:
                project.stash()

    def _print_name(self):
        """Print formatted group name"""
        name_output = colored(self.name, attrs=['bold', 'underline'])
        print(name_output)
