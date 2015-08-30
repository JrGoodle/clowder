"""Model representation of clowder.yaml defaults"""

class Defaults(object):
    """Model class for clowder.yaml defaults"""

    def __init__(self, defaults):
        self.ref = defaults['ref']
        self.remote = defaults['remote']

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'ref': self.ref, 'remote': self.remote}
