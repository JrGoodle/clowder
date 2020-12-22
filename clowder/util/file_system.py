"""File system utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from pathlib import Path

import pygoodle.filesystem as fs
from pygoodle.format import Format

from clowder.log import LOG
from clowder.util.error import ExistingFileError, MissingSourceError


def symlink_clowder_yaml(source: Path, target: Path) -> None:
    """Force symlink creation

    :param Path source: File to create symlink pointing to
    :param Path target: Symlink location
    :raise ExistingFileError:
    :raise MissingSourceError:
    """

    if not target.is_symlink() and target.is_file():
        raise ExistingFileError(f"Found non-symlink file {Format.path(target)} at target path")
    if not Path(target.parent / source).exists():
        raise MissingSourceError(f"Symlink source {Format.path(source)} appears to be missing")
    if target.is_symlink():
        fs.remove_file(target)
    try:
        path = target.parent
        fd = os.open(path, os.O_DIRECTORY)
        os.symlink(source, target, dir_fd=fd)
        os.close(fd)
    except OSError:
        LOG.error(f"Failed to symlink file {Format.path(target)} -> {Format.path(source)}")
        raise
