"""Model representation of clowder.yaml project"""
import os
from termcolor import colored

from clowder.utility.git_utilities import (
    git_litter,
    git_is_detached,
    git_current_branch,
    git_sync_version,
    git_sync,
    git_current_sha,
    # git_validate_repo_state,
    git_is_dirty,
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
                'ref': git_current_sha(self.full_path),
                'remote': self.remote_name}

    def sync(self):
        """Clone project or update latest from upstream"""
        self.print_name()
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)
        else:
            print('Syncing...')
            git_sync(self.full_path, self.ref)

    def sync_version(self, version):
        """Check out fixed version of project"""
        self.print_name()
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)

        print('Checking out fixed version ' + version)
        git_sync_version(self.full_path, version, self.ref)

    def status(self):
        """Print git status of project"""
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            return

        if git_is_dirty(self.full_path):
            color = 'red'
            symbol = '*'
        else:
            color = 'green'
            symbol = ''
        project_output = colored(symbol + self.path, color)

        if git_is_detached(self.full_path):
            current_ref = git_current_sha(self.full_path)
            current_ref_output = colored('(' + current_ref + ')', 'cyan')
        else:
            current_branch = git_current_branch(self.full_path)
            current_ref_output = colored('(' + current_branch + ')', 'cyan')

        print(project_output + ' ' + current_ref_output)

    def print_name(self):
        """Project relative project path in green"""
        project_output = colored(self.path, 'green')
        print(project_output)

    def litter(self):
        """Discard changes in project's repository"""
        self.print_name()
        git_litter(self.full_path)

    def _get_remote_url(self):
        """Return full remote url for project"""
        if self.remote.url.startswith('https://'):
            remote_url = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remote_url = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remote_url = None
        return remote_url

    def validate(self):
        """Validate status of project's repository"""
        # git_validate_repo_state(self.full_path)
