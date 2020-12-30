"""Clowder command line utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path

import pygoodle.filesystem as fs
from pygoodle.console import CONSOLE
from pygoodle.format import Format

from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import MissingFileError

from .file_system import symlink_clowder_yaml


# TODO: Combine this function with link_clowder_yaml_version()
def link_clowder_yaml_default(clowder_dir: Path) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :raise MissingFileError:
    """

    yml_relative_path = Path('.clowder', 'clowder.yml')
    yml_absolute_path = clowder_dir / yml_relative_path
    yaml_relative_path = Path('.clowder', 'clowder.yaml')
    yaml_absolute_path = clowder_dir / yaml_relative_path

    if yml_absolute_path.is_file():
        relative_source_file = yml_relative_path
    elif yaml_absolute_path.is_file():
        relative_source_file = yaml_relative_path
    else:
        message = f"{yml_relative_path} appears to be missing"
        raise MissingFileError(message)

    target_file = clowder_dir / relative_source_file.name

    symlink_output = Format.symlink(target_file, relative_to=ENVIRONMENT.clowder_dir, source=relative_source_file)
    CONSOLE.stdout(f" - Symlink {symlink_output}")

    symlink_clowder_yaml(relative_source_file, target_file)

    existing_file = None
    if target_file.suffix == '.yaml':
        file = clowder_dir / 'clowder.yml'
        if file.exists():
            existing_file = file
    elif target_file.suffix == '.yml':
        file = clowder_dir / 'clowder.yaml'
        if file.exists():
            existing_file = file

    if existing_file is not None and existing_file.is_symlink():
        output_path = Format.path(existing_file, relative_to=ENVIRONMENT.clowder_dir)
        CONSOLE.stdout(f" - Remove previously existing file {output_path}")
        try:
            fs.remove_file(existing_file)
        except OSError:
            LOG.error(f"Failed to remove file {output_path}")
            raise


def link_clowder_yaml_version(clowder_dir: Path, version: str) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :param str version: Version name of clowder yaml file to link
    :raise MissingFileError:
    """

    yml_relative_path = Path('.clowder', 'versions', f'{version}.clowder.yml')
    yml_absolute_path = clowder_dir / yml_relative_path
    yaml_relative_path = Path('.clowder', 'versions', f'{version}.clowder.yaml')
    yaml_absolute_path = clowder_dir / yaml_relative_path

    if yml_absolute_path.is_file():
        relative_source_file = yml_relative_path
    elif yaml_absolute_path.is_file():
        relative_source_file = yaml_relative_path
    else:
        raise MissingFileError(f"{yml_relative_path} appears to be missing")

    target_file = clowder_dir / Format.remove_prefix(relative_source_file.name, f"{version}.")

    CONSOLE.stdout(f" - Symlink {Format.path(Path(target_file.name))} -> {Format.path(relative_source_file)}")

    symlink_clowder_yaml(relative_source_file, target_file)

    existing_file = None
    if target_file.suffix == '.yaml':
        file = clowder_dir / 'clowder.yml'
        if file.exists():
            existing_file = file
    elif target_file.suffix == '.yml':
        file = clowder_dir / 'clowder.yaml'
        if file.exists():
            existing_file = file

    if existing_file is not None and existing_file.is_symlink():
        CONSOLE.stdout(f" - Remove previously existing file {Format.path(existing_file)}")
        try:
            fs.remove_file(existing_file)
        except OSError:
            LOG.error(f"Failed to remove file {Format.path(existing_file)}")
            raise


def print_clowder_yaml() -> None:
    """Print current clowder yaml"""

    if ENVIRONMENT.clowder_yaml.is_file():
        _print_yaml(ENVIRONMENT.clowder_yaml)


def _format_yaml_symlink(yaml_symlink: Path, yaml_file: Path) -> str:
    """Return formatted string for yaml symlink

    :param Path yaml_symlink: Yaml symlink
    :param Path yaml_file: File pointed to by yaml symlink
    :return: Formatted string for yaml symlink
    """

    return f"\n{Format.path(yaml_symlink)} -> {Format.path(yaml_file)}\n"


def _format_yaml_file(yaml_file: Path) -> str:
    """Return formatted string for yaml file

    :param Path yaml_file: Yaml file path
    :return: Formatted string for yaml file
    """

    path = yaml_file.resolve().relative_to(ENVIRONMENT.clowder_dir)
    return f"\n{Format.path(Path(path))}\n"


def _print_yaml(yaml_file: Path) -> None:
    """Private print current clowder yaml file

    :param Path yaml_file: Path to yaml file
    """

    try:
        with yaml_file.open() as raw_file:
            contents = raw_file.read()
            CONSOLE.stdout(contents.rstrip())
    except IOError:
        LOG.error(f"Failed to open file '{yaml_file}'")
        raise


def _print_yaml_path(yaml_file: Path) -> None:
    """Print clowder yaml file path

    :param Path yaml_file: Path to yaml file
    """

    if yaml_file.is_symlink():
        path = yaml_file.resolve().relative_to(ENVIRONMENT.clowder_dir)
        CONSOLE.stdout(_format_yaml_symlink(Path(yaml_file.name), path))
    else:
        CONSOLE.stdout(_format_yaml_file(yaml_file))
