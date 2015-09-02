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

    def __init__(self, root_directory, project, defaults, remotes):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']
        self.full_path = os.path.join(root_directory, self.path)

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults['ref']

        if 'remote' in project:
            remote_name = project['remote']
        else:
            remote_name = defaults['remote']

        for remote in remotes:
            if remote.name == remote_name:
                self.remote = remote

        self.remote_url = self.remote.get_url_prefix() + self.name + ".git"

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': git_current_sha(self.full_path),
                'remote': self.remote.name}

    def groom(self):
        """Discard changes for project"""
        if self.is_dirty():
            print_project_status(self.root_directory, self.path, self.name)
            git_groom(self.full_path)

    def herd(self):
        """Clone project or update latest from upstream"""
        print_project_status(self.root_directory, self.path, self.name)
        if not os.path.isdir(os.path.join(self.full_path, '.git')):
            git_clone_url_at_path(self.remote_url, self.full_path)
        else:
            git_herd(self.full_path, self.ref)

    def herd_version(self, version):
        """Check out fixed version of project"""
        print_project_status(self.root_directory, self.path, self.name)
        if not os.path.isdir(os.path.join(self.full_path, '.git')):
            git_clone_url_at_path(self.remote_url, self.full_path)
        git_herd_version(self.full_path, version, self.ref)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path)

    def meow(self):
        """Print status for project"""
        print_project_status(self.root_directory, self.path, self.name)

    def meow_verbose(self):
        """Print verbose status for project"""
        print_project_status(self.root_directory, self.path, self.name)
        print_verbose_status(self.full_path)

    def run_command(self, command):
        """Run command in project directory"""
        if os.path.isdir(self.full_path):
            print_project_status(self.root_directory, self.path, self.name)
            print_running_command(command)
            subprocess.call(command.split(),
                            cwd=self.full_path)

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty:
            print_project_status(self.root_directory, self.path, self.name)
            git_stash(self.full_path)

    def is_valid(self):
        """Validate status of project"""
        return git_validate_repo_state(self.full_path)

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            print_project_status(self.root_directory, self.path, self.name)
            print_validation(self.full_path)
