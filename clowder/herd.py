import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.projectManager
import clowder.utilities

class Herd(object):

    def __init__(self, rootDirectory, version):
        command = 'repo forall -c git stash'
        clowder.utilities.ex(command)

        self.projectManager = clowder.projectManager.ProjectManager(rootDirectory)
        if version == None:
            self.sync()
            for project in self.projectManager.projects:
                project.repo.git.checkout(project.currentBranch)
        else:
            self.syncVersion(version)

        command = 'repo forall -c git submodule update --init --recursive'
        clowder.utilities.ex(command)
        
        self.updatePeruFile(rootDirectory)

    def sync(self):
        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)

        command = 'repo init -m default.xml'
        clowder.utilities.ex(command)

        command = 'repo sync'
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)

    def syncVersion(self, version):
        command = 'repo init -m ' + version + '.xml'
        clowder.utilities.ex(command)

        command = 'repo sync'
        clowder.utilities.ex(command)

        command = 'repo forall -c git branch ' + version
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout ' + version
        clowder.utilities.ex(command)

    def updatePeruFile(self, rootDirectory):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(rootDirectory, '.clowder/clowder')
        os.chdir(clowderDirectory)
        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)
        command = 'git pull'
        clowder.utilities.ex(command)
        os.chdir(rootDirectory)
        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(rootDirectory, 'peru.yaml')
            if os.path.isfile(peruFile):
                os.remove(peruFile)
            shutil.copy2(newPeruFile, peruFile)
