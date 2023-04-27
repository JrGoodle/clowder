"""Clowder command line utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

import pygoodle.filesystem as fs
from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.yaml import Yaml

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

    source_yaml = Yaml(source_path)
    source_file = source_yaml.update_extension()
    if not source_file.exists():
        raise MissingSourceError(f"Symlink source {Format.path(source_file)} appears to be missing")

    if version is None:
        target_file = clowder_dir / source_file.name
    else:
        target_file = clowder_dir / Format.remove_prefix(source_file.name, f"{version}.")

    if not target_file.is_symlink() and target_file.is_file():
        raise ExistingFileError(f"Found non-symlink file {Format.path(target_file)} at target path")
    target_yaml = Yaml(target_file)
    if target_yaml.path.is_symlink():
        fs.remove(target_yaml.path)
    if target_yaml.path_with_alternate_extension.is_symlink():
        fs.remove(target_yaml.path_with_alternate_extension)

    symlink_output = Format.symlink(target_file, relative_to=clowder_dir, source=source_file)
    CONSOLE.stdout(f' - Symlink {symlink_output}')
    fs.symlink_relative_to(source_file, target_file, relative_to=clowder_dir)


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
