# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os
import shutil
from pathlib import Path

from termcolor import colored

from clowder.error import ClowderExit


def force_symlink(file1: Path, file2: Path) -> None:
    """Force symlink creation

    :param Path file1: File to create symlink pointing to
    :param Path file2: Symlink location
    :raise ClowderExit:
    """

    file1 = str(file1)
    file2 = str(file2)
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


def remove_file(file: Path) -> None:
    """Remove file

    :param Path file: File path to remove
    :raise OSError:
    """

    os.remove(str(file))


def create_backup_file(file: Path) -> None:
    """Copy file to {file}.backup

    :param Path file: File path to copy
    :raise OSError:
    """

    shutil.copyfile(str(file), f"{str(file)}.backup")


def restore_from_backup_file(file: Path) -> None:
    """Copy {file}.backup to file

    :param Path file: File path to copy
    :raise OSError:
    """

    shutil.copyfile(f"{file}.backup", file)


def make_dir(directory: Path) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise OSError:
    """

    if not directory.exists():
        try:
            os.makedirs(str(directory))
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise


def remove_directory(path: Path) -> None:
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
