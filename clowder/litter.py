import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Litter(object):

    def __init__(self):
        command = 'repo forall -c git reset --hard'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo forall -c git clean -fd'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
