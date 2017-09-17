"""Representation of clowder.yaml group"""
from termcolor import colored
from clowder.project import Project

class Group(object):
    """clowder.yaml group class"""

    def __init__(self, root_directory, group, defaults, sources):
        self.name = group['name']
        self.projects = []
        for project in group['projects']:
            self.projects.append(Project(root_directory, project, defaults, sources))
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

    def diff(self):
        """Show git diffs for all projects"""
        self._print_name()
        for project in self.projects:
            project.diff()

    def fetch_all(self):
        """Fetch upstream changes for all projects"""
        self._print_name()
        for project in self.projects:
            project.fetch_all()

    def fetch_silent(self):
        """Silently fetch changes for all projects"""
        for project in self.projects:
            project.fetch_silent()

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

    def prune_all(self, branch, force):
        """Prune local and remote branch"""
        local_branch_exists = self._existing_branch(branch, is_remote=False)
        remote_branch_exists = self._existing_branch(branch, is_remote=True)
        if local_branch_exists or remote_branch_exists:
            self._print_name()
            for project in self.projects:
                project.prune_all(branch, force)

    def prune_local(self, branch, force):
        """Prune local branch"""
        if self._existing_branch(branch, is_remote=False):
            self._print_name()
            for project in self.projects:
                project.prune_local(branch, force)

    def prune_remote(self, branch):
        """Prune remote branch"""
        if self._existing_branch(branch, is_remote=True):
            self._print_name()
            for project in self.projects:
                project.prune_remote(branch)

    def start(self, branch, tracking):
        """Start a new feature branch"""
        self._print_name()
        for project in self.projects:
            project.start(branch, tracking)

    def status(self):
        """Print status for all projects"""
        self._print_name()
        for project in self.projects:
            project.status()

    def stash(self):
        """Stash changes for all projects with changes"""
        if self.is_dirty():
            self._print_name()
            for project in self.projects:
                project.stash()

    def _existing_branch(self, branch, is_remote):
        """Checks whether at least one branch exists"""
        for project in self.projects:
            if is_remote:
                if project.existing_remote_branch(branch):
                    return True
            else:
                if project.existing_local_branch(branch):
                    return True
        return False

    def _print_name(self):
        """Print formatted group name"""
        name_output = colored(self.name, attrs=['bold', 'underline'])
        print(name_output)
