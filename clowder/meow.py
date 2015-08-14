import os, shutil
import sh

from clowder.clowderController import ClowderController

def meow(rootDirectory):
    yamlFile = os.path.join(rootDirectory, 'clowder.yaml')
    if os.path.exists(yamlFile):
        with open(yamlFile) as file:
            clowder = ClowderController(rootDirectory, file)
            clowder.status()
