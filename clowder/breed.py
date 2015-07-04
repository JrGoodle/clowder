import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Breed(object):

    def __init__(self, url):
        command = 'repo init -u ' + url
        clowder.utilities.ex(command)
        command = 'repo sync'
        clowder.utilities.ex(command)
        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)
