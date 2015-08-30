"""Model representation of clowder.yaml project"""
import os
from termcolor import cprint
from clowder.utility.print_utilities import print_repo_status
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_current_sha,
    git_herd,
    git_herd_version
)

class Project(object):
    """Model class for clowder.yaml project"""

    def __init__(self, rootDirectory, project, defaults, remotes):
        self.name = project['name']
        self.path = project['path']
        self.full_path = os.path.join(rootDirectory, self.path)

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults['ref']

        if 'remote' in project:
            self.remote_name = project['remote']
        else:
            self.remote_name = defaults['remote']

        for remote in remotes:
            if remote.name == self.remote_name:
                self.remote = remote

        self.remote_url = self.remote.get_url_prefix() + self.name + ".git"

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': git_current_sha(self.full_path),
                'remote': self.remote_name}

    def herd(self):
        """Clone project or update latest from upstream"""
        print_repo_status(self.full_path, self.name)
        cprint(self.path, 'cyan')
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            git_clone_url_at_path(self.remote_url, self.full_path)
        else:
            git_herd(self.full_path, self.ref)

    def herd_version(self, version):
        """Check out fixed version of project"""
        print_repo_status(self.full_path, self.name)
        cprint(self.path, 'cyan')
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            git_clone_url_at_path(self.remote_url, self.full_path)

        git_herd_version(self.full_path, version, self.ref)
