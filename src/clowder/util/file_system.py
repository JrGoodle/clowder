# -*- coding: utf-8 -*-
"""File system utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import errno
import os
import shutil
from pathlib import Path

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG


def force_symlink(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ClowderError:
    """

    if not target.is_symlink() and target.is_file():
        raise ClowderError(ClowderErrorType.EXISTING_FILE_AT_SYMLINK_TARGET_PATH,
                           fmt.error_existing_file_at_symlink_target_path(str(target)))
    if not source.exists():
        raise ClowderError(ClowderErrorType.SYMLINK_SOURCE_NOT_FOUND,
                           fmt.error_symlink_source_missing(source))
    if target.is_symlink():
        remove_file(target)
    try:
        os.symlink(str(source), str(target))
    except OSError as err:
        LOG_DEBUG('Failed symlink file', err)
        raise ClowderError(ClowderErrorType.FAILED_SYMLINK_FILE,
                           fmt.error_failed_symlink_file(str(target), str(source)), err)


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
                                   fmt.error_directory_exists(str(directory)),
                                   error=err)
            else:
                raise ClowderError(ClowderErrorType.FAILED_CREATE_DIRECTORY,
                                   fmt.error_failed_create_directory(str(directory)),
                                   error=err)


def remove_directory(dir_path: Path) -> None:
    """Remove directory at path

    :param str dir_path: Path to directory to remove
    :raise ClowderError:
    """

    try:
        shutil.rmtree(dir_path)
    except shutil.Error as err:
        LOG_DEBUG('Failed to remove directory', err)
        raise ClowderError(ClowderErrorType.FAILED_REMOVE_DIRECTORY,
                           fmt.error_failed_remove_directory(str(dir_path)),
                           error=err)
