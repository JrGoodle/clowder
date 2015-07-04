import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Play(object):

    def __init__(self, branch):
        command = 'repo forall -c  git stash'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo forall -c git checkout master'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo sync'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo start ' + branch
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
