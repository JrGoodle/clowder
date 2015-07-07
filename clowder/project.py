import os

from git import Repo

class Project(object):

    def __init__(self, rootPath, projectPath):
        self.relativePath = projectPath
        self.absolutePath = os.path.join(rootPath, projectPath)
        self.name = os.path.basename(os.path.normpath(projectPath))
        self.repo = Repo(self.absolutePath)
        self.currentBranch = self.repo.active_branch.name
        self.url = self.repo.remotes.origin.url
