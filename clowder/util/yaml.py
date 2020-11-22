"""Clowder command line utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import pkg_resources
from pathlib import Path

import jsonschema
import yaml as pyyaml

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.environment import ENVIRONMENT
from clowder.error import ExistingFileError, InvalidYamlError, MissingFileError

from .file_system import (
    symlink_clowder_yaml,
    remove_file
)


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

    CONSOLE.stdout(f" - Symlink {fmt.path(Path(target_file.name))} -> {fmt.path(relative_source_file)}")

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
        CONSOLE.stdout(f" - Remove previously existing file {fmt.path(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError:
            CONSOLE.stderr(f"Failed to remove file {fmt.path(existing_file)}")
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

    target_file = clowder_dir / fmt.remove_prefix(relative_source_file.name, f"{version}.")

    CONSOLE.stdout(f" - Symlink {fmt.path(Path(target_file.name))} -> {fmt.path(relative_source_file)}")

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
        CONSOLE.stdout(f" - Remove previously existing file {fmt.path(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError:
            CONSOLE.stderr(f"Failed to remove file {fmt.path(existing_file)}")
            raise


def load_yaml_file(yaml_file: Path, relative_dir: Path) -> dict:
    """Load clowder config from yaml file

    :param Path yaml_file: Path of yaml file to load
    :param Path relative_dir: Directory yaml file is relative to
    :return: YAML python object
    :raise InvalidYamlError:
    """

    try:
        with yaml_file.open() as raw_file:
            parsed_yaml = pyyaml.safe_load(raw_file)
            if parsed_yaml is None:
                config_yaml = yaml_file.relative_to(relative_dir)
                raise InvalidYamlError(f"{fmt.path(yaml_file)}\nNo entries in {fmt.path(config_yaml)}")
            return parsed_yaml
    except pyyaml.YAMLError:
        CONSOLE.stderr(f"Failed to open file '{yaml_file}'")
        raise


def print_clowder_yaml() -> None:
    """Print current clowder yaml"""

    if ENVIRONMENT.clowder_yaml.is_file():
        _print_yaml(ENVIRONMENT.clowder_yaml)


def save_yaml_file(yaml_output: dict, yaml_file: Path) -> None:
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param Path yaml_file: Path to save yaml file
    :raise ExistingFileError:
    """

    if yaml_file.is_file():
        raise ExistingFileError(f"File already exists: {fmt.path(yaml_file)}")

    CONSOLE.stdout(f" - Save yaml to file at {fmt.path(yaml_file)}")
    try:
        with yaml_file.open(mode="w") as raw_file:
            pyyaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=2, sort_keys=False)
    except pyyaml.YAMLError:
        CONSOLE.stderr(f"Failed to save file {fmt.path(yaml_file)}")
        raise


def validate_yaml_file(parsed_yaml: dict, file_path: Path) -> None:
    """Validate yaml file

    :param dict parsed_yaml: Parsed yaml dictionary
    :param Path file_path: Path to yaml file
    """

    json_schema = _load_json_schema(file_path.stem)
    try:
        jsonschema.validate(parsed_yaml, json_schema)
    except jsonschema.exceptions.ValidationError:
        CONSOLE.stderr(f'Yaml json schema validation failed {fmt.invalid_yaml(file_path.name)}\n')
        raise


def yaml_string(yaml_output: dict) -> str:
    """Return yaml string from python data structures

    :param dict yaml_output: YAML python object
    :return: YAML as a string
    """

    try:
        return pyyaml.safe_dump(yaml_output, default_flow_style=False, indent=2, sort_keys=False)
    except pyyaml.YAMLError:
        CONSOLE.stderr(f"Failed to dump yaml file contents",)
        raise


def _format_yaml_symlink(yaml_symlink: Path, yaml_file: Path) -> str:
    """Return formatted string for yaml symlink

    :param Path yaml_symlink: Yaml symlink
    :param Path yaml_file: File pointed to by yaml symlink
    :return: Formatted string for yaml symlink
    """

    return f"\n{fmt.path(yaml_symlink)} -> {fmt.path(yaml_file)}\n"


def _format_yaml_file(yaml_file: Path) -> str:
    """Return formatted string for yaml file

    :param Path yaml_file: Yaml file path
    :return: Formatted string for yaml file
    """

    path = yaml_file.resolve().relative_to(ENVIRONMENT.clowder_dir)
    return f"\n{fmt.path(Path(path))}\n"


def _load_json_schema(file_prefix: str) -> dict:
    """Return json schema file

    :param str file_prefix: File prefix for json schema
    :return: Loaded json dict
    """

    clowder_config_schema = pkg_resources.resource_string(__name__, f"{file_prefix}.schema.json")
    return pyyaml.safe_load(clowder_config_schema)


def _print_yaml(yaml_file: Path) -> None:
    """Private print current clowder yaml file

    :param Path yaml_file: Path to yaml file
    """

    try:
        with yaml_file.open() as raw_file:
            contents = raw_file.read()
            CONSOLE.stdout(contents.rstrip())
    except IOError:
        CONSOLE.stderr(f"Failed to open file '{yaml_file}'")
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
