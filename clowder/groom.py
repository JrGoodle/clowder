import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Groom(object):

    def __init__(self):
        command = 'repo forall -c git fetch --all --prune'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
