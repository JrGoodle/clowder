# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os
import shutil
from pathlib import Path

import clowder.util.formatting as fmt
from clowder import LOG_DEBUG
from clowder.error import ClowderError, ClowderErrorType


def force_symlink(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ClowderError:
    """

    source = str(source)
    target = str(target)
    try:
        os.symlink(source, target)
    except OSError as error:
        LOG_DEBUG('Symlink error', error)
        if error.errno == errno.EEXIST:
            # TODO: Handle possible exceptions thrown here
            os.remove(target)
            os.symlink(source, target)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


def remove_file(file: Path) -> None:
    """Remove file

    :param Path file: File path to remove
    :raise OSError:
    """

    # TODO: Add error logging and handling to throw ClowderError
    os.remove(str(file))


def create_backup_file(file: Path) -> None:
    """Copy file to {file}.backup

    :param Path file: File path to copy
    :raise OSError:
    """

    # TODO: Add error logging and handling to throw ClowderError
    shutil.copyfile(str(file), f"{str(file)}.backup")


def restore_from_backup_file(file: Path) -> None:
    """Copy {file}.backup to file

    :param Path file: File path to copy
    :raise OSError:
    """

    # TODO: Add error logging and handling to throw ClowderError
    shutil.copyfile(f"{file}.backup", file)


def make_dir(directory: Path) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise ClowderError:
    """

    if not directory.exists():
        try:
            os.makedirs(str(directory))
        except OSError as err:
            LOG_DEBUG('Failed to create directory', err)
            if err.errno == errno.EEXIST:
                raise ClowderError(ClowderErrorType.DIRECTORY_EXISTS,
                                   fmt.error_directory_exists(directory))
            else:
                raise ClowderError(ClowderErrorType.FAILED_CREATE_DIRECTORY,
                                   fmt.error_failed_create_directory(directory))


def remove_directory(dir_path: Path) -> None:
    """Remove directory at path

    :param str dir_path: Path to directory to remove
    :raise ClowderError:
    """

    try:
        shutil.rmtree(dir_path)
    except shutil.Error as err:
        LOG_DEBUG('Failed to remove directory', err)
        raise ClowderError(ClowderErrorType.FAILED_REMOVE_DIRECTORY, fmt.error_failed_remove_directory(dir_path))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())
