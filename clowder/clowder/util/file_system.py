# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import errno
import os
import shutil
import sys

from termcolor import colored


def force_symlink(file1, file2):
    """Force symlink creation

    :param str file1: File to create symlink pointing to
    :param str file2: Symlink location
    """

    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)
    except (KeyboardInterrupt, SystemExit):
        os.remove(file2)
        os.symlink(file1, file2)
        sys.exit(1)


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
