"""File system utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import errno
import os
import shutil
from pathlib import Path

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.error import ClowderError, ClowderErrorType


def symlink_clowder_yaml(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ClowderError:
    """

    if not target.is_symlink() and target.is_file():
        message = f"Found non-symlink file {fmt.path(target)} at target path"
        raise ClowderError(ClowderErrorType.EXISTING_FILE_AT_SYMLINK_TARGET_PATH, message)
    if not Path(target.parent / source).exists():
        message = f"Symlink source {fmt.yaml_file(str(source))} appears to be missing"
        raise ClowderError(ClowderErrorType.SYMLINK_SOURCE_NOT_FOUND, message)
    if target.is_symlink():
        remove_file(target)
    try:
        path = target.parent
        fd = os.open(path, os.O_DIRECTORY)
        os.symlink(source, target, dir_fd=fd)
        os.close(fd)
    except OSError:
        CONSOLE.stderr(f"Failed to symlink file {fmt.path(target)} -> {fmt.path(source)}")
        raise


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


# TODO: Remove this in favor of standard Path methods
def make_dir(directory: Path) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :raise ClowderError:
    """

    if not directory.exists():
        try:
            os.makedirs(str(directory))
        except OSError as err:
            if err.errno == errno.EEXIST:
                CONSOLE.stderr(f"Directory already exists at {fmt.path(directory)}")
            else:
                CONSOLE.stderr(f"Failed to create directory {fmt.path(directory)}")
            raise


def remove_directory(dir_path: Path) -> None:
    """Remove directory at path

    :param str dir_path: Path to directory to remove
    :raise ClowderError:
    """

    try:
        shutil.rmtree(dir_path)
    except shutil.Error:
        CONSOLE.stderr(f"Failed to remove directory {fmt.path(dir_path)}")
        raise
