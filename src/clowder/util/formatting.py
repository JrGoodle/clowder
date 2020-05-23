# -*- coding: utf-8 -*-
"""String formatting utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from typing import Optional, Tuple

# noinspection PyPackageRequirements
import yaml
from termcolor import colored
from typing import List, Union

from clowder.error import ClowderExit

from .file_system import symlink_target


ERROR = colored(' - Error:', 'red')


def clowder_command(cmd: str) -> str:
    """Return formatted clowder command name

    :param str cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    return colored(cmd, attrs=['bold'])


def clowder_name(name: str) -> str:
    """Return formatted clowder name

    :param str name: Clowder name
    :return: Formatted clowder name
    :rtype: str
    """

    return colored(name, attrs=['bold'])


def command(cmd: Union[str, List[str]]) -> str:
    """Return formatted command name

    :param cmd: Clowder command name
    :type cmd: str or list[str]
    :return: Formatted clowder command name
    :rtype: str
    """

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return colored(f"$ {command_output}", attrs=['bold'])


def error(err: Exception) -> str:
    """Return error message for generic error

    :param Exception err: Generic error
    :return: Formatted generic error
    :rtype: str
    """

    return f"{ERROR} {str(err)}\n"


def error_command_failed(cmd: Union[str, List[str]]) -> str:
    """Format error message for failed command

    :param cmd: Clowder command name
    :type cmd: str or list[str]
    :return: Formatted clowder command name
    :rtype: str
    """

    return f"{ERROR} Failed to run command {command(cmd)}\n"


def error_duplicate_project_path(path: str, yml: str) -> str:
    """Return formatted error string for duplicate project path

    :param str path: Duplicate project path
    :param str yml: Path to yaml file
    :return: Formatted duplicate remote fork name error
    :rtype: str
    """

    return f"{_yaml_path(yml)}\n{ERROR} Multiple projects with path '{path}'"


def error_empty_yaml(yml: str, name: str) -> str:
    """Return formatted error string for empty clowder.yaml

    :param str yml: Path to yaml file
    :param str name: Name to use in error message
    :return: Formatted empty yaml error
    :rtype: str
    """

    path = _yaml_path(yml)
    file = _yaml_file(name)
    return f"{path}\n{ERROR} No entries in {file}"


def error_file_exists(path: str) -> str:
    """Format error message for already existing file

    :param str path: File path name
    :return: Formatted file exists error
    :rtype: str
    """

    file = path_string(path)
    return f"{ERROR} File already exists {file}"


def error_groups_contains_all(yml: str) -> str:
    """Return formatted error string for invalid 'all' entry in groups list

    :param str yml: Path to yaml file
    :return: Formatted error for groups containing all
    :rtype: str
    """

    path = _yaml_path(yml)
    return f"{path}\n{ERROR} 'groups' cannot contain 'all'"


def error_invalid_ref(ref: str, yml: str) -> str:
    """Return formatted error string for incorrect ref

    :param str ref: Git reference
    :param str yml: Path to yaml file
    :return: Formatted invalid ref error
    """

    path = _yaml_path(yml)
    return f"{path}\n{ERROR} 'ref' value '{ref}' is not formatted correctly"


def error_invalid_clowder_config_yaml() -> str:
    """Return error message for invalid clowder.config.yaml

    :return: Formatted yaml error
    :rtype: str
    """

    file = _yaml_file('clowder.config.yaml')
    return f"{file} appears to be invalid"


def error_invalid_clowder_yaml() -> str:
    """Return error message for invalid clowder.yaml

    :return: Formatted yaml error
    :rtype: str
    """

    file = _yaml_file('clowder.yaml')
    return f"{file} appears to be invalid"


def error_missing_clowder_yaml() -> str:
    """Format error message for missing clowder.yaml

    :return: Formatted missing YAML error
    :rtype: str
    """

    file = _yaml_file('clowder.yaml')
    return f"{file} appears to be missing"


def error_offline() -> str:
    """Return error message for no internet connection

    :return: Offline error message
    :rtype: str
    """

    return f"{ERROR} No available internet connection"


def error_open_file(path: str) -> str:
    """Format error message for failing to open file

    :param str path: File path
    :return: Formatted file error
    :rtype: str
    """

    path = path_string(path)
    return f"{ERROR} Failed to open file '{path}'"


def error_parallel_exception(path: str, *args) -> str:
    """Return formatted error string for parallel error

    :param str path: Clowder file path
    :param args: Method arguments
    :return: Formatted parallel exception error
    :rtype: str
    """

    path = path_string(path)
    return f"{path}\n" + ''.join(args)


def error_remote_already_exists(remote_name: str, remote_url: str, actual_url: str) -> str:
    """Format error message when remote already exists with different url

    :param str remote_name: Remote name
    :param str remote_url: Remote URL
    :param str actual_url: Actual URL
    :return: Formatted remote exists error
    :rtype: str
    """

    remote = remote_string(remote_name)
    return f"{ERROR} Remote {remote} already exists with a different url\n" \
           f"{path_string(actual_url)} should be {path_string(remote_url)}"


def error_remote_dup(fork: str, project: str, remote: str, yml: str) -> str:
    """Return formatted error string for fork with same remote as project

    :param str fork: Fork name
    :param str project: Project name
    :param str remote: Remote name
    :param str yml: Path to yaml file
    :return: Formatted duplicate remote fork name error
    :rtype: str
    """

    path = _yaml_path(yml)
    return f"{path}\n{ERROR} fork '{fork}' and project '{project}' have same remote name '{remote}'"


def error_save_default(name: str) -> str:
    """Format error message for trying to save disallowed version

    :param str name: Version name
    :return: Formatted default version error
    :rtype: str
    """

    return f"{ERROR} Version name '{name}' is not allowed"


def error_save_file(path: str) -> str:
    """Format error message for failing to save file

    :param str path: File path
    :return: Formatted save failure error
    :rtype: str
    """

    path = path_string(path)
    return f"{ERROR} Failed to save file {path}"


def error_save_version_exists(version_name: str, yml: str) -> str:
    """Format error message previous existing saved version

    :param str version_name: Version name
    :param str yml: Path to yaml file
    :return: Formatted version exists error
    :rtype: str
    """

    file = _yaml_file(yml)
    version = version_string(version_name)
    return f"{ERROR} Version '{version}' already exists\n{file}"


def error_source_default_not_found(source: str, yml: str) -> str:
    """Return formatted error string for unknown default source specified

    :param str source: Source name
    :param str yml: Path to yaml file
    :return: Formatted source not found error
    :rtype: str
    """

    return f"{_yaml_path(yml)}\n{ERROR} source '{source}' not found in 'defaults'"


def error_source_not_found(source: str, yml: str, project: str, fork: Optional[str] = None) -> str:
    """Return formatted error string for project with unknown source specified

    :param str source: Source name
    :param str yml: Path to yaml file
    :param str project: Project name
    :param Optional[str] fork: Fork name
    :return: Formatted source not found error
    :rtype: str
    """

    fork_output = ""
    if fork:
        fork_output = f" for fork '{fork}'"

    path = _yaml_path(yml)
    return f"{path}\n{ERROR} source '{source}'{fork_output} specified in project '{project}' not found in 'sources'"


def error_timestamp_not_found() -> str:
    """Return timestamp not found error message

    :return: Formatted timestamp not found error message
    :rtype: str
    """
    return f"{ERROR} Failed to find timestamp\n"


def fork_string(name: str) -> str:
    """Return formatted fork name

    :param str name: Fork name
    :return: Formatted fork name
    :rtype: str
    """

    return colored(name, 'cyan')


def last_path_component(path: str) -> str:
    """Return last path component

    :param str path: Path string
    :return: Last path component
    :rtype: str
    """

    return os.path.basename(os.path.normpath(path))


def options_help_message(options: Tuple[str, ...], message: str) -> str:
    """Help message for groups option

    :param Tuple[str, ...] options: List of options
    :param str message: Help message
    :return: Formatted options help message
    :rtype: str
    """

    if options == [''] or options is None or options == [] or not all(isinstance(n, str) for n in options):
        return message

    help_message = '''
                   {0}:
                   {1}
                   '''

    return help_message.format(message, ', '.join(options))


def path_string(path: str) -> str:
    """Return formatted path

    :param str path: Path name
    :return: Formatted path name
    :rtype: str
    """

    return colored(path, 'cyan')


def ref_string(ref: str) -> str:
    """Return formatted ref name

    :param str ref: Git reference
    :return: Formatted ref name
    :rtype: str
    """

    return colored(f"[{ref}]", 'magenta')


def remote_string(remote: str) -> str:
    """Return formatted remote name

    :param str remote: Remote name
    :return: Formmatted remote name
    :rtype: str
    """

    return colored(remote, 'yellow')


def remove_prefix(text: str, prefix: str) -> str:
    """Remove prefix from a string

    :param str text: String to remove prefix from
    :param str prefix: Prefix to remove
    :return: Text with prefix removed
    :rtype: str
    """

    return text[len(prefix):] if text.startswith(prefix) else text


def save_version_message(version: str, yml: str) -> str:
    """Format message for saving version

    :param str version: Clowder version name
    :param str yml: Path to yaml file
    :return: Formatted version name
    :rtype: str
    """

    version = version_string(version)
    path = path_string(yml)
    return f" - Save version '{version}'\n{path}"


def version_string(version_name: str) -> str:
    """Return formatted string for clowder.yaml version

    :param str version_name: Clowder version name
    :return: Formatted clowder version name
    :rtype: str
    """

    return colored(version_name, attrs=['bold'])


def yaml_string(yaml_output: dict) -> str:
    """Return yaml string from python data structures

    :param dict yaml_output: YAML python object
    :return: YAML as a string
    :rtype: str
    :raise ClowderExit:
    """

    try:
        return yaml.safe_dump(yaml_output, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        print(f"{ERROR} Failed to dump yaml")
        raise ClowderExit(1)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)


def _yaml_path(yml: str) -> str:
    """Returns formatted yaml path

    :param str yml: Path to yaml file
    :return: Formatted YAML path
    :rtype: str
    """

    return path_string(symlink_target(yml))


def _yaml_file(yml: str) -> str:
    """Return formatted string for clowder.yaml file

    :param str yml: Path to yaml file
    :return: Formatted YAML string
    :rtype: str
    """

    return colored(yml, 'cyan')
