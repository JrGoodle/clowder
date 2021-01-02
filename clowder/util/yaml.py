"""Clowder command line utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import os
from pathlib import Path
from typing import Optional

import pygoodle.filesystem as fs
from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.yaml import Yaml

from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import ExistingFileError, MissingSourceError


def link_clowder_yaml(clowder_dir: Path, version: Optional[str] = None) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :param str version: Version name of clowder yaml file to link
    :raise MissingFileError:
    """

    if version is None:
        source_path = clowder_dir / '.clowder' / f'clowder.yml'
    else:
        source_path = clowder_dir / '.clowder' / 'versions' / f'{version}.clowder.yml'

    yaml = Yaml(source_path)
    source_file = yaml.update_extension()

    if version is None:
        target_file = clowder_dir / source_file.name
    else:
        target_file = clowder_dir / Format.remove_prefix(source_file.name, f"{version}.")

    symlink_output = Format.symlink(target_file, relative_to=clowder_dir, source=source_file)
    CONSOLE.stdout(f' - Symlink {symlink_output}')

    symlink_clowder_yaml(source_file.relative_to(clowder_dir), target_file)

    is_ambiguous = yaml.exists and yaml.alternate_extension_exists
    if is_ambiguous and yaml.path_with_alternate_extension.is_symlink():
        fs.remove(yaml.path_with_alternate_extension)


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
    # print(str(source), str(target))
    # Create relative symlink
    try:
        path = target.parent
        fd = os.open(path, os.O_DIRECTORY)
        os.symlink(source, target, dir_fd=fd)
        os.close(fd)
    except OSError:
        LOG.error(f"Failed to symlink file {Format.path(target)} -> {Format.path(source)}")
        raise


def print_clowder_yaml() -> None:
    """Print current clowder yaml"""

    if ENVIRONMENT.clowder_yaml.is_file():
        CONSOLE.stdout(ENVIRONMENT.clowder_yaml.read_text())


# def _print_yaml_path(yaml_file: Path) -> None:
#     """Print clowder yaml file path
#
#     :param Path yaml_file: Path to yaml file
#     """
#
#     if yaml_file.is_symlink():
#         output = f'\n{Format.symlink(yaml_file, relative_to=ENVIRONMENT.clowder_dir)}\n'
#         CONSOLE.stdout(output)
#     else:
#         output = f'\n{Format.path(yaml_file, relative_to=ENVIRONMENT.clowder_dir)}\n'
#         CONSOLE.stdout(output)
