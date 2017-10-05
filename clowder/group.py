"""Representation of clowder.yaml group"""
from termcolor import colored
from clowder.project import Project

# Disable errors shown by pylint for too many branches
# pylint: disable=R0912

class Group(object):
    """clowder.yaml group class"""

    def __init__(self, root_directory, group, defaults, sources):
        self.name = group['name']

        if 'depth' in group:
            self.depth = group['depth']
        else:
            self.depth = defaults['depth']

        if 'recursive' in group:
            self.recursive = group['recursive']
        elif 'recursive' in group:
            self.recursive = defaults['recursive']
        else:
            self.recursive = False

        if 'ref' in group:
            self.ref = group['ref']
        else:
            self.ref = defaults['ref']

        if 'remote' in group:
            self.remote_name = group['remote']
        else:
            self.remote_name = defaults['remote']

        if 'source' in group:
            source_name = group['source']
        else:
            source_name = defaults['source']

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.projects = []
        for project in group['projects']:
            self.projects.append(Project(root_directory, project, group, defaults, sources))
        self.projects.sort(key=lambda project: project.path)

    def branch(self, local=False, remote=False):
        """Print branches for all projects"""
        self._print_name()
        for project in self.projects:
            project.branch(local=local, remote=remote)

    def clean(self, args=None, recursive=False):
        """Discard changes for all projects"""
        self._print_name()
        for project in self.projects:
            project.clean(args=args, recursive=recursive)

    def clean_all(self):
        """Discard all changes for all projects"""
        self._print_name()
        for project in self.projects:
            project.clean_all()

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

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        projects_yaml = [p.get_yaml() for p in self.projects]
        return {'name': self.name, 'projects': projects_yaml}

    def get_yaml_resolved(self):
        """Return python object representation for resolved yaml"""
        projects_yaml = [p.get_yaml(resolved=True) for p in self.projects]
        group = {'name': self.name,
                 'depth': self.depth,
                 'ref': self.ref,
                 'recursive': self.recursive,
                 'remote': self.remote_name,
                 'source': self.source.name,
                 'projects': projects_yaml}
        return group

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

    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branches"""
        if local and remote:
            local_branch_exists = self._existing_branch(branch, is_remote=False)
            remote_branch_exists = self._existing_branch(branch, is_remote=True)
            if local_branch_exists or remote_branch_exists:
                self._print_name()
                for project in self.projects:
                    project.prune(branch, force=force, local=True, remote=True)
        elif local:
            if self._existing_branch(branch, is_remote=False):
                self._print_name()
                for project in self.projects:
                    project.prune(branch, force=force, local=True)
        elif remote:
            if self._existing_branch(branch, is_remote=True):
                self._print_name()
                for project in self.projects:
                    project.prune(branch, remote=True)

    def start(self, branch, tracking):
        """Start a new feature branch"""
        self._print_name()
        for project in self.projects:
            project.start(branch, tracking)

    def status(self, padding):
        """Print status for all projects"""
        self._print_name()
        for project in self.projects:
            project.status(padding)

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
                if project.existing_branch(branch, is_remote=True):
                    return True
            else:
                if project.existing_branch(branch, is_remote=False):
                    return True
        return False

    def _print_name(self):
        """Print formatted group name"""
        name_output = colored(self.name, attrs=['bold', 'underline'])
        print(name_output)
