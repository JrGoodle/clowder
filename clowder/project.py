import os
import sh, yaml

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
        self._create()
        git = sh.git.bake(_cwd=self.fullPath)
        print('Syncing ' + self.name)
        git.pull(_out=process_output)

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

    def _create(self):
        if not os.path.isdir(os.path.join(self.fullPath, '.git')):
            if not os.path.isdir(self.fullPath):
                os.makedirs(self.fullPath)
            print('Cloning ' + self.name + ' at ' + self.path)
            git = sh.git.bake(_cwd=self.fullPath)
            git.init()
            git.remote('add', 'origin', self._getRemoteURL())
            git.fetch(_out=process_output)
            git.checkout('-t', 'origin/master')

    def _getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remoteURL = None
        return remoteURL

def process_output(line):
    print(line)
