import os
import sh

class Project(object):

    def __init__(self, rootDirectory, name, path, ref, remote):
        self.rootDirectory = rootDirectory
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.rootDirectory, self.path)
        self.ref = ref
        self.remote = remote

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
