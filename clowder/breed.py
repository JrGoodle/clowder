import os, shutil

import clowder.utilities

class Breed(object):

    def __init__(self, rootDirectory, sourceURL, sourceFile):
        self.rootDirectory = rootDirectory
        if sourceURL != None:
            self.setupClowderDirectoryFromURL(sourceURL)
        elif sourceFile != None:
            self.setupClowderDirectoryFromFile(sourceFile)
        else:
            print('No valid source for clowder.yaml file')
            exit(1)
        # self.configurePeru()
        self.createSymlinks()

    def setupClowderDirectoryFromURL(self, url):
        dotClowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        os.mkdir(dotClowderDirectory)
        os.chdir(dotClowderDirectory)

        command = 'git clone ' + url + ' repo'
        clowder.utilities.ex(command)

        clowderDirectory = os.path.join(dotClowderDirectory, 'repo')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

    def setupClowderDirectoryFromFile(self, clowderYAML):
        clowderDir = os.path.join(self.rootDirectory, '.clowder')
        os.mkdir(clowderDir)
        repoDir = os.path.join(clowderDir, 'repo')
        os.mkdir(repoDir)
        os.chdir(repoDir)

        command = 'git init'
        clowder.utilities.ex(command)

        shutil.copy2(clowderYAML, os.path.join(repoDir, 'clowder.yaml'))

        command = 'git add clowder.yaml'
        clowder.utilities.ex(command)

        command = 'git commit -m "Add clowder.yaml"'
        clowder.utilities.ex(command)

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
