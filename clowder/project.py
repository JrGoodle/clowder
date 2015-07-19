class Project(object):

    def __init__(self, name, path, ref, remote):
        self.name = name
        self.remote = remote
        self.path = path
        self.ref = ref
        self.remoteURL = self.getRemoteURL()

    def cloneFromURL(self):
        pass

    def sync(self):
        pass

    def create(self):
        pass

    def move(self):
        pass

    def getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url + ":" + self.name
        else:
            remoteURL = None
        return remoteURL
