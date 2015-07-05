import argparse
import os
import sys

from git import Repo

class Project(object):

    def __init__(self, rootPath, projectPath):
        self.relativePath = projectPath.strip()
        self.absolutePath = os.path.join(rootPath.strip(), projectPath.strip())
        self.name = os.path.basename(os.path.normpath(projectPath.strip()))
        self.repo = Repo(self.absolutePath)
        self.url = self.repo.remotes.origin.url
