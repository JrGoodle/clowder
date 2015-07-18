import os, shutil

import clowder.utilities

class Breed(object):

    def __init__(self, rootDirectory, url):
        self.rootDirectory = rootDirectory
        self.setupClowderDirectory(url)
        self.configurePeru()

    def setupClowderDirectory(self, url):
        dotClowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        os.mkdir(dotClowderDirectory)
        os.chdir(dotClowderDirectory)

        command = 'git clone ' + url + ' repo'
        clowder.utilities.ex(command)

        clowderDirectory = os.path.join(dotClowderDirectory, 'repo')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

    def createSymlinks(self):
        pass
        
    def configurePeru(self):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(self.rootDirectory)
        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(self.rootDirectory, 'peru.yaml')
            shutil.copy2(newPeruFile, peruFile)
