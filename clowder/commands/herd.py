import os, shutil

import utilities

class Herd(object):

    def __init__(self, clowder, version, groups):
        # self.projectManager = projectManager.ProjectManager(rootDirectory)
        self.rootDirectory = clowder.rootDirectory
        self.sync(version, groups)
        self.updatePeruFile()

    def sync(self, version, groups):
        command = 'repo forall -c git stash'
        utilities.ex(command)

        command = 'repo forall -c git checkout master'
        utilities.ex(command)

        command = 'repo forall -c git fetch --all --prune'
        utilities.ex(command)

        if groups != None:
            groupsCommand = ' -g all,-notdefault,' + ",".join(groups)
        else:
            groupsCommand = ''

        if version == None and groups != None:
            command = 'repo init -m default.xml' + groupsCommand
            utilities.ex(command)

        if version != None:
            if version == 'master':
                command = 'repo init -m default.xml' + groupsCommand
                utilities.ex(command)
            else:
                command = 'repo init -m ' + version + '.xml' + groupsCommand
                utilities.ex(command)

        command = 'repo sync'
        utilities.ex(command)

        if version == None:
            command = 'repo forall -c git checkout master'
            utilities.ex(command)
            self.restorePreviousBranches()
        elif version == 'master':
            command = 'repo forall -c git checkout master'
            utilities.ex(command)
        else:
            self.createVersionBranch(version)

        command = 'repo forall -c git submodule update --init --recursive'
        utilities.ex(command)

    def createVersionBranch(self, version):
        command = 'repo forall -c git branch ' + version
        utilities.ex(command)

        command = 'repo forall -c git checkout ' + version
        utilities.ex(command)

    def restorePreviousBranches(self):
        # for project in self.projectManager.projects:
            # if os.path.isdir(project.absolutePath):
            #     project.repo.git.checkout(project.currentBranch)
        pass

    def updatePeruFile(self):
        print('Updating peru.yaml')

        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        utilities.ex(command)

        command = 'git pull'
        utilities.ex(command)

        os.chdir(self.rootDirectory)
        newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
        peruFile = os.path.join(self.rootDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            if os.path.isfile(peruFile):
                os.remove(peruFile)
            shutil.copy2(newPeruFile, peruFile)

        if os.path.isfile(peruFile):
            command = 'peru sync -f'
            utilities.ex(command)

    def updatePeru(self):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(self.rootDirectory, '.clowder/clowder')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        utilities.ex(command)

        command = 'git pull'
        utilities.ex(command)

        newPeruFile = os.path.join(self.rootDirectory, 'peru.yaml')
        if os.path.isfile(newPeruFile):
            peruFile = os.path.join(clowderDirectory, 'peru.yaml')
            if os.path.isfile(peruFile):
                os.remove(peruFile)
            shutil.copy2(newPeruFile, peruFile)

        command = 'git add peru.yaml'
        utilities.ex(command)

        command = 'git commit -m "Update peru.yaml"'
        utilities.ex(command)

        command = 'git push'
        utilities.ex(command)
