import os, shutil

import clowder.utilities

class Purr(object):

    def __init__(self, rootDirectory):
        print('Updating peru.yaml')
        clowderDirectory = os.path.join(rootDirectory, '.clowder/clowder')
        os.chdir(clowderDirectory)

        command = 'git fetch --all --prune --tags'
        clowder.utilities.ex(command)

        command = 'git pull'
        clowder.utilities.ex(command)

        newPeruFile = os.path.join(rootDirectory, 'peru.yaml')
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
