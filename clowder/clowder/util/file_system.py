# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import shutil
import sys

from termcolor import colored


def remove_directory(path):
    """Remove directory at path

    :param str path: Path to remove
    """

    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + colored(path, 'cyan'))
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)


def symlink_target(path):
    """Returns target path if input is a symlink, otherwise returns original path

    :param str path: Path of file or symlink
    :return: Target path if input is a symlink, otherwise original path
    :rtype: str
    """

    if os.path.islink(path):
        return os.readlink(path)
    return path
