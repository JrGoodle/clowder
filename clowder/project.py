import os

import git

class Project(object):

    def __init__(self, rootDirectory, name, path, ref, remote):
        self.rootDirectory = rootDirectory
        self.name = name
        self.remote = remote
        self.path = path
        self.ref = ref

    def cloneFromURL(self):
        pass

    def sync(self):
        pass

    def create(self):
        fullPath = os.path.join(self.rootDirectory, self.path)
        if not os.path.isdir(os.path.join(fullPath, '.git')):
            git.Repo.clone_from(self.getRemoteURL(), fullPath)

    # def move(self):
    #     pass

    def getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url + ":" + self.name
        else:
            remoteURL = None
        return remoteURL
