# -*- coding: utf-8 -*-
"""String formatting utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional

# noinspection PyPackageRequirements
import yaml
from termcolor import colored, cprint
from typing import List, Union

from clowder.error.clowder_exit import ClowderExit
from clowder.util.file_system import symlink_target


def clowder_command(cmd: str) -> str:
    """Return formatted clowder command name

    :param str cmd: Clowder command name
    :return: Formatted clowder command name
    :rtype: str
    """

    return colored(cmd, attrs=['bold'])


def command(cmd: Union[str, List[str]]) -> str:
    """Return formatted command name

    :param cmd: Clowder command name
    :type cmd: str or list[str]
    :return: Formatted clowder command name
    :rtype: str
    """

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return colored('$ ' + command_output, attrs=['bold'])


def command_failed_error(cmd: Union[str, List[str]]) -> str:
    """Format error message for failed command

    :param cmd: Clowder command name
    :type cmd: str or list[str]
    :return: Formatted clowder command name
    :rtype: str
    """

    return colored(' - Error: Failed to run command ', 'red') + command(cmd) + '\n'


def depth_error(depth: int, yml: str) -> str:
    """Return formatted error string for invalid depth

    :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param str yml: Path to yaml file
    :return: Formatted depth error
    :rtype: str
    """

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored('depth', attrs=['bold'])
    output_2 = colored(' must be a positive integer\n', 'red') + colored('depth: ' + str(depth), attrs=['bold'])
    return output_1 + output_2


def empty_yaml_error(yml: str) -> str:
    """Return formatted error string for empty clowder.yaml

    :param str yml: Path to yaml file
    :return: Formatted empty yaml error
    :rtype: str
    """

    return yaml_path(yml) + colored(' - Error: No entries in ', 'red') + yaml_file('clowder.yaml')


def error(err: Exception) -> str:
    """Return error message for generic error

    :param Exception err: Generic error
    :return: Formatted generic error
    :rtype: str
    """

    return f'{str(err)}\n'


def file_exists_error(path: str) -> str:
    """Format error message for already existing file

    :param str path: File path name
    :return: Formatted file exists error
    :rtype: str
    """

    return colored(' - Error: File already exists\n', 'red') + get_path(path)


def fork_string(name: str) -> str:
    """Return formatted fork name

    :param str name: Fork name
    :return: Formatted fork name
    :rtype: str
    """

    return colored(name, 'cyan')


def groups_contains_all_error(yml: str) -> str:
    """Return formatted error string for invalid entry in collection

    :param str yml: Path to yaml file
    :return: Formatted missing entries error
    :rtype: str
    """

    output_1 = colored(' - Error: ', 'red')
    output_2 = colored('groups', attrs=['bold'])
    output_3 = colored(' cannot contain ', 'red')
    output_4 = colored('all', attrs=['bold'])
    return f'{yaml_path(yml)}{output_1}{output_2}{output_3}{output_4}'


def invalid_protocol_error(protocol: str, yml: str) -> str:
    """Return formatted error string for incorrect protocol

    :param str protocol: Git protocol
    :param str yml: Path to yaml file
    :return: Formatted invalid ref error
    """

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored('protocol', attrs=['bold'])
    output_2 = colored(' value ', 'red') + colored(protocol, attrs=['bold'])
    output_3 = colored(' is not valid', 'red')
    return output_1 + output_2 + output_3


def invalid_ref_error(ref: str, yml: str) -> str:
    """Return formatted error string for incorrect ref

    :param str ref: Git reference
    :param str yml: Path to yaml file
    :return: Formatted invalid ref error
    """

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored('ref', attrs=['bold'])
    output_2 = colored(' value ', 'red') + colored(ref, attrs=['bold'])
    output_3 = colored(' is not formatted correctly', 'red')
    return output_1 + output_2 + output_3


def invalid_yaml_error() -> str:
    """Return error message for invalid clowder.yaml

    :return: Formatted yaml error
    :rtype: str
    """

    file = yaml_file('clowder.yaml')
    return f'{file} appears to be invalid'


def missing_entries_error(name: str, yml: str) -> str:
    """Return formatted error string for invalid entry in collection

    :param str name: Entry name
    :param str yml: Path to yaml file
    :return: Formatted missing entries error
    :rtype: str
    """

    return yaml_path(yml) + colored(' - Error: Missing entries in ', 'red') + colored(name, attrs=['bold'])


def missing_entry_error(entry: str, name: str, yml: str) -> str:
    """Return formatted error string for missing entry in dictionary

    :param str entry: Name of entry to check
    :param str name:  Name of entry to print if missing
    :param str yml: Path to yaml file
    :return: Formatted missing entry in dictionary error
    :rtype: str
    """

    output_1 = yaml_path(yml) + colored(' - Error: Missing ', 'red') + colored(str(entry), attrs=['bold'])
    output_2 = colored(' in ', 'red') + colored(str(name), attrs=['bold'])
    return output_1 + output_2


def missing_imported_yaml_error(path: str, yml: str) -> str:
    """Return formatted error string for missing imported clowder.yaml

    :param str path: File path
    :param str yml: Path to yaml file
    :return: Formatted missing YAML error
    :rtype: str
    """

    return yaml_path(yml) + colored(' - Error: Missing imported file\n', 'red') + get_path(path)


def missing_yaml_error() -> str:
    """Format error message for missing clowder.yaml

    :return: Formatted missing YAML error
    :rtype: str
    """

    file = yaml_file('clowder.yaml')
    return f'{file} appears to be missing'


def offline_error() -> str:
    """Return error message for no internet connection

    :return: Offline error message
    :rtype: str
    """

    return colored('No available internet connection\n', 'red')


def open_file_error(path: str) -> str:
    """Format error message for failing to open file

    :param str path: File path
    :return: Formatted file error
    :rtype: str
    """

    return colored(' - Error: Failed to open file\n', 'red') + get_path(path)


def parallel_exception_error(path: str, *args) -> str:
    """Return formatted error string for parallel error

    :param str path: Clowder file path
    :param args: Method arguments
    :return: Formatted parallel exception error
    :rtype: str
    """

    return get_path(path) + '\n' + ''.join(args)


def get_path(path: str) -> str:
    """Return formatted path

    :param str path: Path name
    :return: Formatted path name
    :rtype: str
    """

    return colored(path, 'cyan')


def recursive_import_error(depth: int) -> str:
    """Format error message for too many recursive imports

    :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :return: Formatted too many recursive imports error
    :rtype: str
    """

    output_1 = colored(' - Error: Too many recursive imports', 'red')
    output_2 = colored(str(depth), attrs=['bold'])
    return f'{output_1}\nMax imports: {output_2}'


def ref_string(ref: str) -> str:
    """Return formatted ref name

    :param str ref: Git reference
    :return: Formatted ref name
    :rtype: str
    """

    return colored(f'[{ref}]', 'magenta')


def remote_already_exists_error(remote_name: str, remote_url: str, actual_url: str) -> str:
    """Format error message when remote already exists with different url

    :param str remote_name: Remote name
    :param str remote_url: Remote URL
    :param str actual_url: Actual URL
    :return: Formatted remote exists error
    :rtype: str
    """

    output_1 = colored(' - Remote ', 'red') + remote_string(remote_name)
    output_2 = colored(' already exists with a different url', 'red')
    output_3 = f'\n{get_path(actual_url)} should be {get_path(remote_url)}\n'
    return output_1 + output_2 + output_3


def remote_name_error(fork: str, project: str, remote: str) -> str:
    """Return formatted error string for fork with same remote as project

    :param str fork: Fork name
    :param str project: Project name
    :param str remote: Remote name
    :return: Formatted duplicate remote fork name error
    :rtype: str
    """

    output_1 = colored(' - Error: fork ', 'red') + colored(fork, attrs=['bold'])
    output_2 = colored(' and project ', 'red') + colored(project, attrs=['bold'])
    output_3 = colored(' have same remote name ', 'red') + colored(remote, attrs=['bold'])
    return output_1 + output_2 + output_3


def remote_string(remote: str) -> str:
    """Return formatted remote name

    :param str remote: Remote branch name
    :return: Formmatted remote branch name
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


def save_default_error(name: str) -> str:
    """Format error message for trying to save 'default' version

    :param str name: Version name
    :return: Formatted default version error
    :rtype: str
    """

    output_1 = colored(' - Error: Version name ', 'red') + colored(name, attrs=['bold'])
    output_2 = colored(' is not allowed', 'red')
    return output_1 + output_2


def save_file_error(path: str) -> str:
    """Format error message for failing to save file

    :param str path: File path
    :return: Formatted save failure error
    :rtype: str
    """

    return colored(' - Error: Failed to save file', 'red') + get_path(path)


def save_version(version_name: str, yml: str) -> str:
    """Format message for saving version

    :param str version_name: Clowder version name
    :param str yml: Path to yaml file
    :return: Formatted version name
    :rtype: str
    """

    return ' - Save version ' + version(version_name) + '\n' + get_path(yml)


def save_version_exists_error(version_name: str, yml: str) -> str:
    """Format error message previous existing saved version

    :param str version_name: Version name
    :param str yml: Path to yaml file
    :return: Formatted version exists error
    :rtype: str
    """

    output_1 = colored(' - Error: Version ', 'red') + version(version_name)
    output_2 = colored(' already exists', 'red') + yaml_file(yml)
    return output_1 + output_2


def source_not_found_error(source: str, project: str, fork: Optional[str] = None) -> str:
    """Return formatted error string for project with unknown source specified

    :param str source: Source name
    :param str project: Project name
    :param Optional[str] fork: Fork name
    :return: Formatted source not found error
    :rtype: str
    """

    output_1 = colored(' - Error: source ', 'red') + colored(source, attrs=['bold'])
    output_2 = ''
    if fork:
        output_2 = colored(' for fork ', 'red') + colored(fork, attrs=['bold'])
    output_3 = colored(' specified in project ', 'red') + colored(project, attrs=['bold'])
    output_4 = colored(' not found in sources', 'red')
    return output_1 + output_2 + output_3 + output_4


def type_error(name: str, yml: str, type_name: str) -> str:
    """Return formatted error string for value with wrong type

    :param str name: Value name
    :param str yml: Path to yaml file
    :param str type_name: Type name
    :return: Formatted incorrect type error
    :rtype: str
    """

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored(name, attrs=['bold'])
    output_2 = colored(' type should be ', 'red') + colored(type_name, 'yellow')
    return output_1 + output_2


def unknown_entry_error(name: str, collection: dict, yml: str) -> str:
    """Return formatted error string for unknown entry in collection

    :param str name: Entry name
    :param dict collection: Entries collection
    :param str yml: Path to yaml file
    :return: Formatted unknown entry error
    :rtype: str
    """

    if len(collection) > 1:
        output_1 = yaml_path(yml) + colored(' - Error: Unknown entries in ', 'red')
    else:
        output_1 = yaml_path(yml) + colored(' - Error: Unknown entry in ', 'red')
    dict_entries = ''.join('{}: {}\n'.format(key, val) for key, val in sorted(collection.items())).rstrip()
    output_2 = colored('\n\n' + str(dict_entries), attrs=['bold'])
    return output_1 + colored(name, attrs=['bold']) + output_2


def version(version_name: str) -> str:
    """Return formatted string for clowder.yaml version

    :param str version_name: Clowder version name
    :return: Formatted clowder version name
    :rtype: str
    """

    return colored(version_name, attrs=['bold'])


def yaml_path(yml: str) -> str:
    """Returns formatted yaml path

    :param str yml: Path to yaml file
    :return: Formatted YAML path
    :rtype: str
    """

    return get_path(symlink_target(yml)) + '\n'


def yaml_file(yml: str) -> str:
    """Return formatted string for clowder.yaml file

    :param str yml: Path to yaml file
    :return: Formatted YAML string
    :rtype: str
    """

    return colored(yml, 'cyan')


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
        cprint('Failed to dump yaml', 'red')
        raise ClowderExit(1)
    except (KeyboardInterrupt, SystemExit):
        raise ClowderExit(1)
