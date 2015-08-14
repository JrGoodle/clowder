import os, shutil
import sh

class Breed(object):

    def __init__(self, rootDirectory, url):
        self.rootDirectory = rootDirectory
        self.setupClowderDirectory(url)
        # self.configurePeru()
        self.createSymlinks()

    def setupClowderDirectory(self, url):
        dotClowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        os.mkdir(dotClowderDirectory)

        git = sh.git.bake(_cwd=dotClowderDirectory)
        git.clone(url, 'repo')

        clowderDirectory = os.path.join(dotClowderDirectory, 'repo')
        git = sh.git.bake(_cwd=clowderDirectory)
        git.fetch('--all', '--prune', '--tags')

    def createSymlinks(self):
        os.chdir(self.rootDirectory)
        clowderYAML = '.clowder/repo/clowder.yaml'
        peruYAML = '.clowder/repo/peru.yaml'
        if os.path.isfile(clowderYAML):
            os.symlink(clowderYAML, 'clowder.yaml')
        if os.path.isfile(peruYAML):
            os.symlink(peruYAML, 'peru.yaml')

    def configurePeru(self):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(self.rootDirectory)
        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(self.rootDirectory, 'peru.yaml')
            shutil.copy2(newPeruFile, peruFile)
