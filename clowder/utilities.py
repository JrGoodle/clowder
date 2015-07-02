# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import sys

import ev.log

def ex(command):
    r = Popen(command, stderr=PIPE, shell=True)
    stdout, stderr = r.communicate()
    if r.poll() != 0:
        ev.log.toFile('The command "{0}" failed: {1}'.format(command, stderr))
        ev.log.toFile('Aborting.\n')
        sys.exit()

def unknownArg(command, arg):
    ev.log.toFile('Unknown argument for "{0}": "{1}"\n'.format(command, arg))
    ev.log.toFile('\t ❓  Dunno what that means...  ¯\_(ツ)_/¯\n')
    ev.log.toFile('Aborting.\n')
    sys.exit()
