"""Model representation of clowder.yaml project"""
import os

from clowder.utility.git_utilities import (
    git_sync_version,
    git_sync,
    git_status,
    get_current_sha,
    clone_git_url_at_path
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
            self.ref = defaults.ref

        if 'remote' in project:
            self.remote_name = project['remote']
        else:
            self.remote_name = defaults.remote

        for remote in remotes:
            if remote.name == self.remote_name:
                self.remote = remote

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': get_current_sha(self.full_path),
                'remote': self.remote_name}

    def sync(self):
        """Clone project or update latest from upstream"""
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)
        else:
            print('Syncing ' + self.name)
            print('At Path ' + self.full_path)
            git_sync(self.full_path, self.ref)
        print("")

    def sync_version(self, version):
        """Check out fixed version of project"""
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)
        else:
            git_sync(self.full_path, self.ref)

        print('Checking out fixed version of ' + self.name)
        git_sync_version(self.full_path, version, self.ref)
        print("")

    def status(self):
        """Print git status of project"""
        print(self.path)
        git_status(self.full_path)
        print("")

    def _get_remote_url(self):
        """Return full remote url for project"""
        if self.remote.url.startswith('https://'):
            remote_url = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remote_url = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remote_url = None
        return remote_url
