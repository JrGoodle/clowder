"""Representation of clowder.yaml group"""

from __future__ import print_function

from termcolor import colored

from clowder.model.project import Project


class Group(object):
    """clowder.yaml group class"""

    def __init__(self, root_directory, group, defaults, sources):

        self.name = group['name']
        self.depth = group.get('depth', defaults['depth'])
        self.recursive = group.get('recursive', defaults.get('recursive', False))
        self.timestamp_author = group.get('timestamp_author', defaults.get('timestamp_author', None))
        self.ref = group.get('ref', defaults['ref'])
        self.remote_name = group.get('remote', defaults['remote'])
        source_name = group.get('source', defaults['source'])

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.projects = []
        for project in group['projects']:
            self.projects.append(Project(root_directory, project, group, defaults, sources))
        self.projects.sort(key=lambda p: p.path)

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
        if self.timestamp_author:
            group['timestamp_author'] = self.timestamp_author
        return group

    def is_dirty(self):
        """Check if group has dirty project(s)"""

        return any([project.is_dirty() for project in self.projects])

    def is_valid(self):
        """Validate status of all projects"""

        return all([project.is_valid() for project in self.projects])

    def print_existence_message(self):
        """Print existence validation message for projects in group"""
        if not self.projects_exist():
            self.print_name()
            for project in self.projects:
                project.print_exists()

    def print_name(self):
        """Print formatted group name"""
        name_output = colored(self.name, attrs=['bold', 'underline'])
        print(name_output)

    def print_validation(self):
        """Print validation message for projects in group"""
        if not self.is_valid():
            self.print_name()
            for project in self.projects:
                project.print_validation()

    def projects_exist(self):
        """Validate existence status of all projects"""

        return all([project.exists() for project in self.projects])

    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branches"""
        if local and remote:
            local_branch_exists = self._existing_branch(branch, is_remote=False)
            remote_branch_exists = self._existing_branch(branch, is_remote=True)
            if local_branch_exists or remote_branch_exists:
                self.print_name()
                for project in self.projects:
                    project.prune(branch, force=force, local=True, remote=True)
        elif local:
            if self._existing_branch(branch, is_remote=False):
                self.print_name()
                for project in self.projects:
                    project.prune(branch, force=force, local=True)
        elif remote:
            if self._existing_branch(branch, is_remote=True):
                self.print_name()
                for project in self.projects:
                    project.prune(branch, remote=True)

    def status(self, padding):
        """Print status for all projects"""
        self.print_name()
        for project in self.projects:
            project.status(padding)

    def stash(self):
        """Stash changes for all projects with changes"""
        if self.is_dirty():
            self.print_name()
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
