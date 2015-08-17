import os
import sh, yaml

from clowder.utilities import process_output, cloneGitUrlAtPath, truncateGitRef

class Project(object):
    def __init__(self, rootDirectory, project, defaults, remotes):
        self.name = project['name']
        self.path = project['path']
        self.fullPath = os.path.join(rootDirectory, self.path)

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults.ref

        if 'remote' in project:
            self.remoteName = project['remote']
        else:
            self.remoteName = defaults.remote

        for remote in remotes:
            if remote.name == self.remoteName:
                self.remote = remote

    def getYAML(self):
        return {'name': self.name,
                'path': self.path,
                'ref': self.getCurrentSHA(),
                'remote': self.remoteName}

    def sync(self):
        gitPath = os.path.join(self.fullPath, '.git')
        if not os.path.isdir(gitPath):
            cloneGitUrlAtPath(self._getRemoteURL(), self.fullPath)
        else:
            git = sh.git.bake(_cwd=self.fullPath)
            print('Syncing ' + self.name)
            print('At Path ' + self.fullPath)
            git.fetch('--all', '--prune', '--tags', _out=process_output)
            projectRef = truncateGitRef(self.ref)
            # print('currentBranch: ' + self.getCurrentBranch())
            # print('projectRef: ' + projectRef)
            if self.getCurrentBranch() == projectRef:
                git.pull(_out=process_output)
            else:
                print('Not on default branch')

    def syncVersion(self, version):
        git = sh.git.bake(_cwd=self.fullPath)
        print('Checking out fixed version of ' + self.name)
        git.fetch('--all', '--prune', '--tags', _out=process_output)
        git.checkout('-b', 'fix/' + version, self.ref, _out=process_output)

    def status(self):
        git = sh.git.bake(_cwd=self.fullPath)
        print(self.path)
        print(git.status())

    def getCurrentBranch(self):
        git = sh.git.bake(_cwd=self.fullPath)
        return str(git('rev-parse', '--abbrev-ref', 'HEAD')).rstrip('\n')

    def getCurrentSHA(self):
        git = sh.git.bake(_cwd=self.fullPath)
        return str(git('rev-parse', 'HEAD')).rstrip('\n')

    def _getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remoteURL = None
        return remoteURL
