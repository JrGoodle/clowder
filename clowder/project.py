"""Model representation of clowder.yaml project"""
import os
from clowder.utility.print_utilities import (
    print_project_status,
    print_validation,
    print_verbose_status
)
from clowder.utility.clowder_utilities import (
    groom,
    herd,
    validate_repo_state
)
from clowder.utility.git_utilities import (
    git_current_sha,
    git_is_dirty,
    git_stash,
)


class Project(object):
    """Model class for clowder.yaml project"""

    def __init__(self, root_directory, project, defaults, sources):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults['ref']

        if 'remote' in project:
            self.remote_name = project['remote']
        else:
            self.remote_name = defaults['remote']

        if 'source' in project:
            source_name = project['source']
        else:
            source_name = defaults['source']

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.url = self.source.get_url_prefix() + self.name + ".git"

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': git_current_sha(self.full_path()),
                'remote': self.remote_name,
                'source': self.source.name}

    def groom(self):
        """Discard changes for project"""
        if self.is_dirty():
            self._print_status()
            groom(self.full_path())

    def herd(self):
        """Clone project or update latest from upstream"""
        self._print_status()
        herd(self.full_path(), self.ref, self.remote_name, self.url)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path())

    def meow(self):
        """Print status for project"""
        self._print_status()

    def meow_verbose(self):
        """Print verbose status for project"""
        self._print_status()
        print_verbose_status(self.full_path())

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            self._print_status()
            git_stash(self.full_path())

    def is_valid(self):
        """Validate status of project"""
        return validate_repo_state(self.full_path())

    def _print_status(self):
        """Print formatted project status"""
        print_project_status(self.root_directory, self.path, self.name)

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            self._print_status()
            print_validation(self.full_path())
