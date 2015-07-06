import sys
import os
import shutil
import subprocess

from git import Repo

import clowder.log
import clowder.utilities

class Breed(object):

    def __init__(self, rootDirectory, url, groups):
        self.rootDirectory = rootDirectory

        command = 'repo init -u ' + url
        if not groups == None:
            command += ' -g all,-notdefault,' + ','.join(groups)
        clowder.utilities.ex(command)

        command = 'repo sync'
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)

        command = 'repo forall -c git submodule update --init --recursive'
        clowder.utilities.ex(command)

        self.setupClowderDirectory(url)
        self.configurePeru()

    def setupClowderDirectory(self, url):
        dotClowderDirectory = os.path.join(self.rootDirectory, '.clowder')
        os.mkdir(dotClowderDirectory)
        os.chdir(dotClowderDirectory)

        command = 'git clone ' + url + ' clowder'
        clowder.utilities.ex(command)

        clowderDirectory = os.path.join(dotClowderDirectory, 'clowder')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

    def configurePeru(self):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(self.rootDirectory)
        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(self.rootDirectory, 'peru.yaml')
            shutil.copy2(newPeruFile, peruFile)
