import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Purr(object):

    def __init__(self):
        command = 'repo forall -c git push'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
