import os
import shutil

from git import Repo

import clowder.log
import clowder.utilities

class Fix(object):

    def __init__(self, version):
        versionManifest = version + '.xml'

        command = 'repo manifest -o .clowder/clowder/' + versionManifest + ' -r'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        os.chdir('.clowder/clowder')

        command = 'git add ' + versionManifest
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git commit -m "Add manifest ' + version + '"'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git push'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git tag ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'git push origin ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
