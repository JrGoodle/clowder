import argparse
import sys

class Project(object):

    def __init__(self, name, path, url):
        self.name = name
        self.path = path
        self.url = url
