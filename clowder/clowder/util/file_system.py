"""File system utilities"""

from __future__ import print_function

import os
import shutil
import sys

from termcolor import colored


def remove_directory(path):
    """Remove directory at path"""

    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + colored(path, 'cyan'))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def symlink_target(path):
    """Returns target path if input is a symlink"""

    if os.path.islink(path):
        return os.readlink(path)
    return path
