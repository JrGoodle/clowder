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
        self.create()
        git = sh.git.bake(_cwd=self.fullPath)
        git.pull()

    def create(self):
        if not os.path.isdir(os.path.join(self.fullPath, '.git')):
            if not os.path.isdir(self.fullPath):
                os.makedirs(self.fullPath)
            git = sh.git.bake(_cwd=self.fullPath)
            git.clone(self._getRemoteURL(), '.')

    def _getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url[6:] + ":" + self.name
        else:
            remoteURL = None
        return remoteURL
