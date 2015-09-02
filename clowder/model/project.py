"""Model representation of clowder.yaml project"""
import os, subprocess
from clowder.utility.print_utilities import (
    print_project_status,
    print_running_command,
    print_validation,
    print_verbose_status
)
from clowder.utility.git_utilities import (
    git_groom,
    git_stash,
    git_is_dirty
)
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_current_sha,
    git_herd,
    git_herd_version,
    git_validate_repo_state
)


class Project(object):
    """Model class for clowder.yaml project"""

    def __init__(self, root_directory, project, defaults, sources):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']
        self.full_path = os.path.join(root_directory, self.path)

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

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': git_current_sha(self.full_path),
                'remote': self.source.name}

    def groom(self):
        """Discard changes for project"""
        if self.is_dirty():
            self._print_status()
            git_groom(self.full_path)

    def herd(self):
        """Clone project or update latest from upstream"""
        self._print_status()
        if not os.path.isdir(os.path.join(self.full_path, '.git')):
            git_clone_url_at_path(self.url, self.full_path)
        else:
            git_herd(self.full_path, self.ref)

    def herd_version(self, version):
        """Check out fixed version of project"""
        self._print_status()
        if not os.path.isdir(os.path.join(self.full_path, '.git')):
            git_clone_url_at_path(self.url, self.full_path)
        git_herd_version(self.full_path, version, self.ref)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path)

    def meow(self):
        """Print status for project"""
        self._print_status()

    def meow_verbose(self):
        """Print verbose status for project"""
        self._print_status()
        print_verbose_status(self.full_path)

    def run_command(self, command):
        """Run command in project directory"""
        if os.path.isdir(self.full_path):
            self._print_status()
            print_running_command(command)
            subprocess.call(command.split(),
                            cwd=self.full_path)

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty:
            self._print_status()
            git_stash(self.full_path)

    def is_valid(self):
        """Validate status of project"""
        return git_validate_repo_state(self.full_path)

    def _print_status(self):
        """Print formatted project status"""
        print_project_status(self.root_directory, self.path, self.name)

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            self._print_status()
            print_validation(self.full_path)
