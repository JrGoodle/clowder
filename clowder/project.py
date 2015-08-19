"""Model representation of clowder.yaml project"""
import os
import sh
# Disable errors shown by pylint for sh.git
# pylint: disable=E1101

from clowder.utilities import process_output, clone_git_url_at_path, truncate_git_ref

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
                'ref': self.get_current_sha(),
                'remote': self.remote_name}

    def sync(self):
        """Clone project or update latest from upstream"""
        git_path = os.path.join(self.full_path, '.git')
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)
        else:
            git = sh.git.bake(_cwd=self.full_path)
            print('Syncing ' + self.name)
            print('At Path ' + self.full_path)
            git.fetch('--all', '--prune', '--tags', _out=process_output)
            project_ref = truncate_git_ref(self.ref)
            # print('currentBranch: ' + self.get_current_branch())
            # print('project_ref: ' + project_ref)
            if self.get_current_branch() != project_ref:
                print('Not on default branch')
                print('Stashing current changes')
                git.stash()
                print('Checking out ' + project_ref)
                git.checkout(project_ref)
            print('Pulling latest changes')
            git.pull(_out=process_output)


    def sync_version(self, version):
        """Check out fixed version of project"""
        git_path = os.path.join(self.full_path, '.git')
        git = sh.git.bake(_cwd=self.full_path)
        if not os.path.isdir(git_path):
            clone_git_url_at_path(self._get_remote_url(), self.full_path)
        else:
            git.fetch('--all', '--prune', '--tags', _out=process_output)
        print('Checking out fixed version of ' + self.name)
        git.checkout('-b', 'fix/' + version, self.ref, _out=process_output)

    def status(self):
        """Print git status of project"""
        git = sh.git.bake(_cwd=self.full_path)
        print(self.path)
        print(git.status())

    def get_current_branch(self):
        """Return currently checked out branch of project"""
        git = sh.git.bake(_cwd=self.full_path)
        return str(git('rev-parse', '--abbrev-ref', 'HEAD')).rstrip('\n')

    def get_current_sha(self):
        """Return current git sha for checked out commit"""
        git = sh.git.bake(_cwd=self.full_path)
        return str(git('rev-parse', 'HEAD')).rstrip('\n')

    def _get_remote_url(self):
        """Return full remote url for project"""
        if self.remote.url.startswith('https://'):
            remote_url = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remote_url = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remote_url = None
        return remote_url
