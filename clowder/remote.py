import os
import sh, yaml

class Remote(object):
    def __init__(self, remote):
        self.name = remote['name']
        self.url = remote['url']

    def getYAML(self):
        return {'name': self.name, 'url': self.url}
