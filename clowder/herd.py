import os, shutil
import sh

from clowder.clowderController import ClowderController

def herd(rootDirectory):
    repoDir = os.path.join(rootDirectory, '.clowder/repo')
    git = sh.git.bake(_cwd=repoDir)
    git.pull()

    yamlFile = os.path.join(rootDirectory, 'clowder.yaml')
    if os.path.exists(yamlFile):
        with open(yamlFile) as file:
            clowder = ClowderController(rootDirectory, file)
    clowder.sync()
