import os
import sh, yaml

class Defaults(object):
    def __init__(self, defaults):
        self.ref = defaults['ref']
        self.remote = defaults['remote']
        self.groups = defaults['groups']

    def getYAML(self):
        return {'ref': self.ref, 'remote': self.remote, 'groups':self.groups}
