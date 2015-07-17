import os

import clowder.utilities

class Nest(object):

    def __init__(self):
        clowder.utilities.removeAllFilesInDirectory(os.getcwd())
