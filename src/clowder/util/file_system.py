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


def force_symlink(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ClowderExit:
    """

    source = str(source)
    target = str(target)
    try:
        os.symlink(source, target)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(target)
            os.symlink(source, target)
    except (KeyboardInterrupt, SystemExit):
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
