import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Litter(object):

    def __init__(self, projects):
        command = 'repo forall ' + " ".join(projects) + ' -c git reset --hard'
        clowder.utilities.ex(command)

        command = 'repo forall ' + " ".join(projects) + ' -c git clean -fd'
        clowder.utilities.ex(command)
