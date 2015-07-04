# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import sys

import clowder.log

def ex(command):
    r = Popen(command, stderr=PIPE, shell=True)
    stdout, stderr = r.communicate()
    if r.poll() != 0:
        clowder.log.toFile('The command "{0}" failed: {1}'.format(command, stderr))
        clowder.log.toFile('Aborting.\n')
        sys.exit()

def unknownArg(command, arg):
    clowder.log.toFile('Unknown argument for "{0}": "{1}"\n'.format(command, arg))
    clowder.log.toFile('\t ❓  Dunno what that means...  ¯\_(ツ)_/¯\n')
    clowder.log.toFile('Aborting.\n')
    sys.exit()
