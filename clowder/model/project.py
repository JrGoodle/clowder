class Project(object):

    def __init__(self, name, path, ref, remote):
        self.name = name
        self.path = path
        self.ref = ref
        self.remote = remote

    def sync(self):
        pass

    def create(self):
        pass

    def move(self):
        pass
