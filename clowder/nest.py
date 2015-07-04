import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Nest(object):

    def __init__(self):
        clowder.utilities.removeAllFilesInDirectory(os.getcwd())
