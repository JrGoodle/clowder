# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os
import shutil

from termcolor import colored

from clowder.error import ClowderExit


def force_symlink(file1: str, file2: str) -> None:
    """Force symlink creation

    :param str file1: File to create symlink pointing to
    :param str file2: Symlink location
    :raise ClowderExit:
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
        raise ClowderExit(1)


def make_dir(directory: str) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise OSError:
    """

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise


def remove_directory(path: str) -> None:
    """Remove directory at path

    :param str path: Path to remove
    :raise ClowderExit:
    """

    try:
        shutil.rmtree(path)
    except shutil.Error:
        message = colored(" - Failed to remove directory ", 'red')
        print(message + colored(path, 'cyan'))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def symlink_target(path: str) -> str:
    """Returns target path if input is a symlink, otherwise returns original path

    :param str path: Path of file or symlink
    :return: Target path if input is a symlink, otherwise original path
    :rtype: str
    """

    if os.path.islink(path):
        return os.readlink(path)
    return path
