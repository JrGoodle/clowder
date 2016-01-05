"""Representation of clowder.yaml fork"""

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, name, path, remote):
        self.name = name
        self.path = path
        self.remote = remote

    def fetch(self):
        """Fetch remote data from fork"""
        # git_fetch_fork(path, remote)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote}
