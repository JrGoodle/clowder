"""File system utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import errno
import os
import shutil
from pathlib import Path

import clowder.util.formatting as fmt
from clowder.util.console import CONSOLE
from clowder.util.error import ExistingFileError, MissingSourceError


def symlink_clowder_yaml(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ExistingFileError:
    :raise MissingSourceError:
    """

    if not target.is_symlink() and target.is_file():
        raise ExistingFileError(f"Found non-symlink file {fmt.path(target)} at target path")
    if not Path(target.parent / source).exists():
        raise MissingSourceError(f"Symlink source {fmt.path(source)} appears to be missing")
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
    """

    os.remove(str(file))


def create_backup_file(file: Path) -> None:
    """Copy file to {file}.backup

    :param Path file: File path to copy
    """

    shutil.copyfile(str(file), f"{str(file)}.backup")


def restore_from_backup_file(file: Path) -> None:
    """Copy {file}.backup to file

    :param Path file: File path to copy
    """

    shutil.copyfile(f"{file}.backup", file)


def make_dir(directory: Path, check: bool = True) -> None:
    """Make directory if it doesn't exist

    :param str directory: Directory path to create
    :param bool check: Whether to raise exceptions
    """

    if directory.exists():
        return

    try:
        os.makedirs(str(directory))
    except OSError as err:
        if err.errno == errno.EEXIST:
            CONSOLE.stderr(f"Directory already exists at {fmt.path(directory)}")
        else:
            CONSOLE.stderr(f"Failed to create directory {fmt.path(directory)}")
        if check:
            raise


def remove_directory(dir_path: Path, check: bool = True) -> None:
    """Remove directory at path

    :param str dir_path: Path to directory to remove
    :param bool check: Whether to raise errors
    """

    try:
        shutil.rmtree(dir_path)
    except shutil.Error:
        CONSOLE.stderr(f"Failed to remove directory {fmt.path(dir_path)}")
        if check:
            raise
