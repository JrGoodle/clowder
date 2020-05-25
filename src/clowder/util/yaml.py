# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
import pkg_resources
from pathlib import Path

# noinspection PyPackageRequirements
import jsonschema
# noinspection PyPackageRequirements
import yaml as pyyaml

import clowder.util.formatting as fmt
from clowder import CLOWDER_CONFIG_DIR, CLOWDER_CONFIG_YAML, CLOWDER_DIR, CLOWDER_YAML, LOG_DEBUG
from clowder.error import (
    ClowderError,
    ClowderErrorType,
    ClowderConfigYAMLErrorType,
    ClowderYAMLErrorType
)

from .file_system import (
    force_symlink,
    remove_file
)


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
        raise ClowderError(ClowderYAMLErrorType.MISSING_YAML,
                           fmt.error_missing_linked_clowder_yaml(yml_relative_path))

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

    if existing_file is not None:
        print(f" - Remove previously existing file {fmt.path_string(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError as err:
            LOG_DEBUG('Failed to remove file', err)
            ClowderError(ClowderErrorType.FAILED_REMOVE_FILE, fmt.error_failed_remove_file(existing_file))


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
        raise ClowderError(ClowderYAMLErrorType.MISSING_YAML,
                           fmt.error_missing_linked_clowder_yaml(yml_relative_path))

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

    if existing_file is not None:
        print(f" - Remove previously existing file {fmt.path_string(existing_file)}")
        try:
            remove_file(existing_file)
        except OSError as err:
            LOG_DEBUG('Failed to remove file', err)
            raise ClowderError(ClowderErrorType.FAILED_REMOVE_FILE, fmt.error_failed_remove_file(existing_file))


def load_clowder_config_yaml() -> dict:
    """Load clowder config from yaml file

    :return: YAML python object
    :rtype: dict
    :raise ClowderError:
    """

    try:
        with open(CLOWDER_CONFIG_YAML) as raw_file:
            parsed_yaml = pyyaml.safe_load(raw_file)
            if parsed_yaml is None:
                config_yaml = CLOWDER_CONFIG_YAML.relative_to(CLOWDER_CONFIG_DIR)
                raise ClowderError(ClowderConfigYAMLErrorType.EMPTY_FILE,
                                   fmt.error_empty_yaml(CLOWDER_CONFIG_YAML, config_yaml))
            return parsed_yaml
    except pyyaml.YAMLError as err:
        LOG_DEBUG('Failed to load yaml file', err)
        raise ClowderError(ClowderConfigYAMLErrorType.OPEN_FILE, fmt.error_open_file(CLOWDER_CONFIG_YAML))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


def load_clowder_yaml() -> dict:
    """Load clowder from yaml file

    :return: YAML python object
    :rtype: dict
    :raise ClowderError:
    """

    try:
        with CLOWDER_YAML.open() as raw_file:
            parsed_yaml = pyyaml.safe_load(raw_file)
            if parsed_yaml is None:
                clowder_yaml = CLOWDER_YAML.relative_to(CLOWDER_DIR)
                raise ClowderError(ClowderYAMLErrorType.EMPTY_FILE, fmt.error_empty_yaml(CLOWDER_YAML, clowder_yaml))
            return parsed_yaml
    except pyyaml.YAMLError:
        raise ClowderError(ClowderYAMLErrorType.OPEN_FILE, fmt.error_open_file(CLOWDER_YAML))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


def print_yaml() -> None:
    """Print current clowder yaml"""

    if CLOWDER_YAML.is_file():
        _print_yaml(CLOWDER_YAML)


def save_yaml(yaml_output: dict, yaml_file: Path) -> None:
    """Save yaml file to disk

    :param dict yaml_output: Parsed YAML python object
    :param Path yaml_file: Path to save yaml file
    :raise ClowderError:
    """

    if yaml_file.is_file():
        raise ClowderError(ClowderErrorType.FILE_EXISTS, fmt.error_file_exists(yaml_file))

    try:
        with yaml_file.open(mode="w") as raw_file:
            print(f" - Save yaml to file at {fmt.path_string(yaml_file)}")
            pyyaml.safe_dump(yaml_output, raw_file, default_flow_style=False, indent=4)
    except pyyaml.YAMLError as err:
        LOG_DEBUG('Failed to save yaml file', err)
        raise ClowderError(ClowderErrorType.FAILED_SAVE_FILE, fmt.error_save_file(yaml_file))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


def validate_clowder_config_yaml(parsed_yaml: dict) -> None:
    """Validate clowder config yaml file

    :raise ClowderError:
    """

    json_schema = _load_clowder_config_json_schema()
    try:
        jsonschema.validate(parsed_yaml, json_schema)
    except jsonschema.exceptions.ValidationError as err:
        error_message = f"{fmt.error_invalid_yaml_file(CLOWDER_CONFIG_YAML.name)}\n{fmt.ERROR} {err.message}"
        raise ClowderError(ClowderConfigYAMLErrorType.JSONSCHEMA_VALIDATION_FAILED, error_message)


def validate_clowder_yaml(parsed_yaml: dict) -> None:
    """Validate clowder yaml file

    :param dict parsed_yaml: Parsed yaml dictionary
    :raise ClowderError:
    """

    json_schema = _load_clowder_json_schema()
    parsed_yaml_content_validation_copy = copy.deepcopy(parsed_yaml)
    try:
        jsonschema.validate(parsed_yaml, json_schema)
    except jsonschema.exceptions.ValidationError as err:
        error_message = f"{fmt.error_invalid_yaml_file(CLOWDER_YAML.name)}\n{fmt.ERROR} {err.message}"
        raise ClowderError(ClowderYAMLErrorType.JSONSCHEMA_VALIDATION_FAILED, error_message)

    _validate_yaml_contents(parsed_yaml_content_validation_copy, CLOWDER_YAML)


def _format_yaml_symlink(yaml_symlink: Path, yaml_file: Path) -> str:
    """Return formatted string for yaml symlink

    :param Path yaml_symlink: Yaml symlink
    :param Path yaml_file: File pointed to by yaml symlink
    :return: Formatted string for yaml symlink
    :rtype: str
    """

    return f"\n{fmt.path_string(yaml_symlink)} -> {fmt.path_string(yaml_file)}\n"


def _format_yaml_file(yaml_file: Path) -> str:
    """Return formatted string for yaml file

    :param Path yaml_file: Yaml file path
    :return: Formatted string for yaml file
    :rtype: str
    """

    path = yaml_file.resolve().relative_to(CLOWDER_DIR)
    return f"\n{fmt.path_string(Path(path))}\n"


def _load_clowder_config_json_schema() -> dict:
    """Return json schema file for clowder config yaml file

    :return: Loaded json dict
    :rtype: dict
    """

    clowder_config_schema = pkg_resources.resource_string(__name__, "clowder.config.schema.json")
    return pyyaml.safe_load(clowder_config_schema)


def _load_clowder_json_schema() -> dict:
    """Return json schema file for clowder yaml file

    :return: Loaded json dict
    :rtype: dict
    """

    clowder_schema = pkg_resources.resource_string(__name__, "clowder.schema.json")
    return pyyaml.safe_load(clowder_schema)


def _print_yaml(yaml_file: Path) -> None:
    """Private print current clowder yaml file

    :param Path yaml_file: Path to yaml file
    :raise ClowderError:
    """

    try:
        with yaml_file.open() as raw_file:
            contents = raw_file.read()
            print('-' * 80)
            _print_yaml_path(yaml_file)
            print(contents)
    except IOError as err:
        LOG_DEBUG('Failed to open file', err)
        raise ClowderError(ClowderErrorType.FAILED_OPEN_FILE, fmt.error_open_file(yaml_file))
    except (KeyboardInterrupt, SystemExit):
        raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


def _print_yaml_path(yaml_file: Path) -> None:
    """Print clowder yaml file path

    :param Path yaml_file: Path to yaml file
    """

    if yaml_file.is_symlink():
        path = yaml_file.resolve().relative_to(CLOWDER_DIR)
        print(_format_yaml_symlink(Path(yaml_file.name), path))
    else:
        print(_format_yaml_file(yaml_file))


# TODO: Should probably just go ahead and move this logic into ClowderController to reduce duplication
def _validate_yaml_contents(yaml: dict, yaml_file: Path) -> None:
    """Validate contents in clowder loaded from yaml file

    :param dict yaml: Parsed YAML python object
    :param Path yaml_file: Path to yaml file
    """

    err_prefix = f"{fmt.error_invalid_yaml_file(yaml_file.name)}\n{fmt.ERROR} "

    sources = []
    for source in yaml['sources']:
        sources.append(source['name'])

    defaults = yaml['defaults']
    if 'remote' not in defaults:
        defaults['remote'] = 'origin'

    # Validate default source is defined in sources
    if defaults['source'] not in sources:
        message = f"{err_prefix}{fmt.error_source_default_not_found(defaults['source'], yaml_file)}"
        raise ClowderError(ClowderYAMLErrorType.SOURCE_NOT_FOUND, message)

    projects = []
    projects_with_forks = []
    for p in yaml['projects']:
        project = {'name': p['name'],
                   'path': p.get('path', str(Path(p['name']).name))}
        if 'remote' in p:
            project['remote'] = p['remote']
        if 'source' in p:
            # Validate custom project source is defined in sources
            if p['source'] not in sources:
                message = f"{err_prefix}{fmt.error_source_not_found(p['source'], yaml_file, project['name'])}"
                raise ClowderError(ClowderYAMLErrorType.SOURCE_NOT_FOUND, message)
        projects.append(project)
        if 'fork' in p:
            f = p['fork']
            fork = {'name': f['name']}
            if 'remote' in f:
                fork['remote'] = f['remote']
            if 'source' in f:
                # Validate custom fork source is defined in sources
                if f['source'] not in sources:
                    message = f"{err_prefix}{fmt.error_source_not_found(f['source'], yaml_file, project['name'])}"
                    raise ClowderError(ClowderYAMLErrorType.SOURCE_NOT_FOUND, message)
            project['fork'] = fork
            projects_with_forks.append(project)

    # Validate projects and forks have different remote names
    for project in projects_with_forks:
        fork = project['fork']
        default_remote = defaults['remote']
        if 'remote' in project and 'remote' in fork:
            if project['remote'] == fork['remote']:
                message = fmt.error_remote_dup(fork['name'], project['name'], project['remote'], yaml_file)
                message = f"{err_prefix}{message}"
                raise ClowderError(ClowderYAMLErrorType.DUPLICATE_REMOTE_NAME, message)
        elif 'remote' in project:
            if project['remote'] == default_remote:
                message = fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)
                message = f"{err_prefix}{message}"
                raise ClowderError(ClowderYAMLErrorType.DUPLICATE_REMOTE_NAME, message)
        elif 'remote' in fork:
            if fork['remote'] == default_remote:
                message = fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)
                message = f"{err_prefix}{message}"
                raise ClowderError(ClowderYAMLErrorType.DUPLICATE_REMOTE_NAME, message)
        else:
            message = f"{err_prefix}{fmt.error_remote_dup(fork['name'], project['name'], default_remote, yaml_file)}"
            raise ClowderError(ClowderYAMLErrorType.DUPLICATE_REMOTE_NAME, message)

    # Validate projects don't share share directories
    paths = [str(Path(p['path']).resolve()) for p in projects]
    duplicate = fmt.check_for_duplicates(paths)
    if duplicate is not None:
        message = f"{err_prefix}{fmt.error_duplicate_project_path(Path(duplicate), yaml_file)}"
        raise ClowderError(ClowderYAMLErrorType.DUPLICATE_PATH, message)
