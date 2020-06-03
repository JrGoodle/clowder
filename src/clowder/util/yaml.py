# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import pkg_resources
from pathlib import Path

# noinspection PyPackageRequirements
import jsonschema
# noinspection PyPackageRequirements
import yaml as pyyaml

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

from .file_system import (
    force_symlink,
    remove_file
)


# TODO: Combine this function with link_clowder_yaml_version()
def link_clowder_yaml_default(clowder_dir: Path) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :raise ClowderError:
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
        raise ClowderError(ClowderErrorType.YAML_MISSING_FILE,
                           fmt.error_missing_file(yml_relative_path))

    source_file = clowder_dir / relative_source_file
    target_file = clowder_dir / source_file.name

    print(f" - Symlink {fmt.path_string(Path(target_file.name))} -> {fmt.path_string(relative_source_file)}")

    force_symlink(source_file, clowder_dir / target_file)

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
        print(f" - Remove previously existing file {fmt.path_string(str(existing_file))}")
        try:
            remove_file(existing_file)
        except OSError as err:
            LOG_DEBUG('Failed to remove file', err)
            ClowderError(ClowderErrorType.FAILED_REMOVE_FILE,
                         fmt.error_failed_remove_file(str(existing_file)),
                         error=err)


def link_clowder_yaml_version(clowder_dir: Path, version: str) -> None:
    """Create symlink pointing to clowder yaml file

    :param Path clowder_dir: Directory to create symlink in
    :param str version: Version name of clowder yaml file to link
    :raise ClowderError:
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
        raise ClowderError(ClowderErrorType.YAML_MISSING_FILE,
                           fmt.error_missing_file(yml_relative_path))

    source_file = clowder_dir / relative_source_file
    target_file = clowder_dir / fmt.remove_prefix(source_file.name, f"{version}.")

    print(f" - Symlink {fmt.path_string(Path(target_file.name))} -> {fmt.path_string(relative_source_file)}")

    force_symlink(source_file, target_file)

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
        print(f" - Remove previously existing file {fmt.path_string(str(existing_file))}")
        try:
            remove_file(existing_file)
        except OSError as err:
            LOG_DEBUG('Failed to remove file', err)
            raise ClowderError(ClowderErrorType.FAILED_REMOVE_FILE,
                               fmt.error_failed_remove_file(str(existing_file)),
                               error=err)


def load_yaml_file(yaml_file: Path, relative_dir: Path) -> dict:
    """Load clowder config from yaml file

    :param Path yaml_file: Path of yaml file to load
    :param Path relative_dir: Directory yaml file is relative to
    :return: YAML python object
    :rtype: dict
    :raise ClowderError:
    """

    try:
        with open(str(yaml_file)) as raw_file:
            parsed_yaml = pyyaml.safe_load(raw_file)
            if parsed_yaml is None:
                config_yaml = yaml_file.relative_to(relative_dir)
                raise ClowderError(ClowderErrorType.YAML_EMPTY_FILE,
                                   fmt.error_empty_yaml(yaml_file, config_yaml))
            return parsed_yaml
    except pyyaml.YAMLError as err:
        LOG_DEBUG('Failed to load yaml file', err)
        raise ClowderError(ClowderErrorType.OPEN_FILE,
                           fmt.error_open_file(str(yaml_file)),
                           error=err)


def print_clowder_yaml() -> None:
    """Print current clowder yaml"""

    if ENVIRONMENT.clowder_yaml.is_file():
        _print_yaml(ENVIRONMENT.clowder_yaml)


def save_yaml_file(yaml_output: dict, yaml_file: Path) -> None:
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param Path yaml_file: Path to save yaml file
    :raise ClowderError:
    """

    if yaml_file.is_file():
        raise ClowderError(ClowderErrorType.FILE_EXISTS,
                           fmt.error_file_exists(str(yaml_file)))

    print(f" - Save yaml to file at {fmt.path_string(str(yaml_file))}")
    try:
        with yaml_file.open(mode="w") as raw_file:
            pyyaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=2)
    except pyyaml.YAMLError as err:
        LOG_DEBUG('Failed to save yaml file', err)
        raise ClowderError(ClowderErrorType.FAILED_SAVE_FILE,
                           fmt.error_save_file(str(yaml_file)),
                           error=err)


def validate_yaml_file(parsed_yaml: dict, file_path: Path) -> None:
    """Validate yaml file

    :param dict parsed_yaml: Parsed yaml dictionary
    :param Path file_path: Path to yaml file
    :raise ClowderError:
    """

    json_schema = _load_json_schema(file_path.stem)
    try:
        jsonschema.validate(parsed_yaml, json_schema)
    except jsonschema.exceptions.ValidationError as err:
        LOG_DEBUG('Yaml json schema validation failed', err)
        messages = [f"{fmt.error_invalid_yaml_file(file_path.name)}",
                    f"{fmt.ERROR} {err.message}"]
        raise ClowderError(ClowderErrorType.YAML_JSONSCHEMA_VALIDATION_FAILED, messages)


def yaml_string(yaml_output: dict) -> str:
    """Return yaml string from python data structures

    :param dict yaml_output: YAML python object
    :return: YAML as a string
    :rtype: str
    :raise ClowderError:
    """

    try:
        return pyyaml.safe_dump(yaml_output, default_flow_style=False, indent=2)
    except pyyaml.YAMLError as err:
        LOG_DEBUG('Failed to dump yaml file contents', err)
        raise ClowderError(ClowderErrorType.FAILED_YAML_DUMP,
                           f"{fmt.ERROR} Failed to dump yaml file contents",
                           error=err)


def _format_yaml_symlink(yaml_symlink: Path, yaml_file: Path) -> str:
    """Return formatted string for yaml symlink

    :param Path yaml_symlink: Yaml symlink
    :param Path yaml_file: File pointed to by yaml symlink
    :return: Formatted string for yaml symlink
    :rtype: str
    """

    return f"\n{fmt.path_string(str(yaml_symlink))} -> {fmt.path_string(str(yaml_file))}\n"


def _format_yaml_file(yaml_file: Path) -> str:
    """Return formatted string for yaml file

    :param Path yaml_file: Yaml file path
    :return: Formatted string for yaml file
    :rtype: str
    """

    path = yaml_file.resolve().relative_to(ENVIRONMENT.clowder_dir)
    return f"\n{fmt.path_string(Path(path))}\n"


def _load_json_schema(file_prefix: str) -> dict:
    """Return json schema file

    :param str file_prefix: File prefix for json schema
    :return: Loaded json dict
    :rtype: dict
    """

    clowder_config_schema = pkg_resources.resource_string(__name__, f"{file_prefix}.schema.json")
    return pyyaml.safe_load(clowder_config_schema)


def _print_yaml(yaml_file: Path) -> None:
    """Private print current clowder yaml file

    :param Path yaml_file: Path to yaml file
    :raise ClowderError:
    """

    try:
        with yaml_file.open() as raw_file:
            contents = raw_file.read()
            print(contents.rstrip())
    except IOError as err:
        LOG_DEBUG('Failed to open file', err)
        raise ClowderError(ClowderErrorType.FAILED_OPEN_FILE,
                           fmt.error_open_file(str(yaml_file)),
                           error=err)


def _print_yaml_path(yaml_file: Path) -> None:
    """Print clowder yaml file path

    :param Path yaml_file: Path to yaml file
    """

    if yaml_file.is_symlink():
        path = yaml_file.resolve().relative_to(ENVIRONMENT.clowder_dir)
        print(_format_yaml_symlink(Path(yaml_file.name), path))
    else:
        print(_format_yaml_file(yaml_file))
