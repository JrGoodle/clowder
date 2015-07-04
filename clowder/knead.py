import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Knead(object):

    def __init__(self):
        command = 'repo diff'
        clowder.utilities.ex(command)
