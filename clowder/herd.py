import os, shutil
import sh

from clowder.clowderController import ClowderController
import clowder.utilities

class Herd(object):

    def __init__(self, rootDirectory):
        self.rootDirectory = rootDirectory
        self.updateClowderRepo()
        yamlFile = os.path.join(self.rootDirectory, 'clowder.yaml')
        if os.path.exists(yamlFile):
            with open(yamlFile) as file:
                self.clowder = ClowderController(self.rootDirectory, file)
        self.clowder.sync()

    def updateClowderRepo(self):
        repoDir = os.path.join(self.rootDirectory, '.clowder/repo')
        git = sh.git.bake(_cwd=repoDir)
        git.pull()
