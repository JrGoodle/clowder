"""Clowder utilities"""

from __future__ import print_function

import shutil
import sys

from termcolor import colored

import clowder.utility.formatting as fmt


def remove_directory(path):
    """Remove directory at path"""
    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + fmt.path(path))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
