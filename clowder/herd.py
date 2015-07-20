import os, shutil

import clowder.utilities

class Herd(object):

    def __init__(self, clowderController, version, groups):
        self.clowderController = clowderController
        self.rootDirectory = clowderController.rootDirectory
        self.sync(version, groups)
        self.updatePeruFile()

    def update(self):
        pass

    def sync(self, version, groups):
        # for all projects
            # fetch -all --tags --prune
            # check if current branch is default branch
                # check if no changes in working tree
                    # update branch to current upstream

        if version == None and groups != None:
            pass

        if version == None:
            pass
        else:
            self.createVersionBranch(version)

        # for all projects update submodules

    def createVersionBranch(self, version):
        command = 'repo forall -c git branch ' + version
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout ' + version
        clowder.utilities.ex(command)

    def restorePreviousBranches(self):
        # for project in self.projectManager.projects:
            # if os.path.isdir(project.absolutePath):
            #     project.repo.git.checkout(project.currentBranch)
        pass

    def updateClowderRepo(self):
        repoDir = os.path.join(self.rootDirectory, '.clowder/repo')
        os.chdir(repoDir)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

        command = 'git pull'
        clowder.utilities.ex(command)

    def updatePeruFile(self):
        print('Updating peru.yaml')

        self.updateClowderRepo()

        os.chdir(self.rootDirectory)
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')

        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        peruFile = os.path.join(self.rootDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            if os.path.isfile(peruFile):
                os.remove(peruFile)
            shutil.copy2(newPeruFile, peruFile)

        if os.path.isfile(peruFile):
            command = 'peru sync -f'
            clowder.utilities.ex(command)

    def updatePeru(self):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

        command = 'git pull'
        clowder.utilities.ex(command)

        newPeruFile = os.path.join(self.rootDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(clowderDirectory, 'peru.yaml')
            if os.path.isfile(peruFile):
                os.remove(peruFile)
            shutil.copy2(newPeruFile, peruFile)

        command = 'git add peru.yaml'
        clowder.utilities.ex(command)

        command = 'git commit -m "Update peru.yaml"'
        clowder.utilities.ex(command)

        command = 'git push'
        clowder.utilities.ex(command)
