import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Herd(object):

    def __init__(self, version):
        if version == None:
            self.sync()
        else:
            self.syncVersion(version)

    def sync(self):
        command = 'repo forall -c git stash'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo sync'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

    def syncVersion(self, version):
        command = 'repo forall -c git stash'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo init -m ' + version + '.xml'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo sync'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo forall -c git branch ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout ' + version
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
