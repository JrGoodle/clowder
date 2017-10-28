"""String formatting utilities"""

import sys

import yaml
from termcolor import colored, cprint

from clowder.util.file_system import symlink_target


def clowder_command(cmd):
    """Return formatted clowder command name"""

    return colored(cmd, attrs=['bold'])


def command(cmd):
    """Return formatted command name"""

    command_output = " ".join(cmd) if isinstance(cmd, list) else cmd
    return colored('$ ' + command_output, attrs=['bold'])


def command_failed_error(cmd):
    """Format error message for failed command"""

    return colored(' - Error: Failed to run command ', 'red') + command(cmd) + '\n'


def depth_error(depth, yml):
    """Return formatted error string for invalid depth"""

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored('depth', attrs=['bold'])
    output_2 = colored(' must be a positive integer\n', 'red') + colored('depth: ' + str(depth), attrs=['bold'])
    return output_1 + output_2


def empty_yaml_error(yml):
    """Return formatted error string for empty clowder.yaml"""

    return yaml_path(yml) + colored(' - Error: No entries in ', 'red') + yaml_file('clowder.yaml')


def error(err):
    """Return error message for generic error"""

    return str(err) + '\n'


def file_exists_error(path):
    """Format error message for already existing file"""

    return colored(' - Error: File already exists\n', 'red') + get_path(path)


def fork_string(name):
    """Return formatted fork name"""

    return colored(name, 'cyan')


def group_name(name):
    """Print formatted group name"""

    return colored(name, attrs=['bold', 'underline'])


def invalid_ref_error(ref, yml):
    """Return formatted error string for incorrect ref"""

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored('ref', attrs=['bold'])
    output_2 = colored(' value ', 'red') + colored(ref, attrs=['bold'])
    output_3 = colored(' is not formatted correctly', 'red')
    return output_1 + output_2 + output_3


def invalid_yaml_error():
    """Return error message for invalid clowder.yaml"""

    return '\n' + yaml_file('clowder.yaml') + ' appears to be invalid'


def missing_entries_error(name, yml):
    """Return formatted error string for invalid entry in collection"""

    output_1 = yaml_path(yml) + colored(' - Error: Missing entries in ', 'red')
    output_2 = colored(name, attrs=['bold'])
    return output_1 + output_2


def missing_entry_error(entry, name, yml):
    """Return formatted error string for missing entry in dictionary"""

    output_1 = yaml_path(yml) + colored(' - Error: Missing ', 'red') + colored(str(entry), attrs=['bold'])
    output_2 = colored(' in ', 'red') + colored(str(name), attrs=['bold'])
    return output_1 + output_2


def missing_imported_yaml_error(path, yml):
    """Return formatted error string for missing imported clowder.yaml"""

    return yaml_path(yml) + colored(' - Error: Missing imported file\n', 'red') + get_path(path)


def missing_yaml_error():
    """Format error message for missing clowder.yaml"""

    return yaml_file('clowder.yaml') + ' appears to be missing'


def offline_error():
    """Return error message for no internet connection"""

    colored('No available internet connection\n', 'red')


def open_file_error(path):
    """Format error message for failing to open file"""

    return colored(' - Error: Failed to open file\n', 'red') + get_path(path)


def parallel_exception_error(path, *args):
    """Return formatted error string for parallel error"""

    return get_path(path) + '\n' + ''.join(args)


def get_path(path):
    """Return formatted path"""

    return colored(path, 'cyan')


def recursive_import_error(depth):
    """Format error message for too many recursive imports"""

    output_1 = colored(' - Error: Too many recursive imports\n', 'red')
    output_2 = colored(str(depth), attrs=['bold'])
    return output_1 + 'Max imports: ' + output_2


def ref_string(ref):
    """Return formatted ref name"""

    return colored('(' + ref + ')', 'magenta')


def remote_already_exists_error(remote_name, remote_url, actual_url):
    """Format error message when remote already exists with different url"""

    output_1 = colored(' - Remote ', 'red') + remote_string(remote_name)
    output_2 = colored(' already exists with a different url', 'red')
    output_3 = '\n' + get_path(actual_url) + ' should be ' + get_path(remote_url) + '\n'
    return output_1 + output_2 + output_3


def remote_name_error(fork, project, remote):
    """Return formatted error string for fork with same remote as project"""

    output_1 = colored(' - Error: fork ', 'red') + colored(fork, attrs=['bold'])
    output_2 = colored(' and project ', 'red') + colored(project, attrs=['bold'])
    output_3 = + colored(' have same remote name ', 'red') + colored(remote, attrs=['bold'])
    return output_1 + output_2 + output_3


def remote_string(remote):
    """Return formatted remote name"""

    return colored(remote, 'yellow')


def remove_prefix(text, prefix):
    """Remove prefix from a string"""

    return text[len(prefix):] if text.startswith(prefix) else text


def save_default_error(name):
    """Format error message for trying to save 'default' version"""
    output_1 = colored(' - Error: Version name ', 'red') + colored(name, attrs=['bold'])
    output_2 = colored(' is not allowed\n', 'red')
    return output_1 + output_2


def save_file_error(path):
    """Format error message for failing to save file"""

    return colored(' - Error: Failed to save file\n', 'red') + get_path(path)


def save_version(version_name, yml):
    """Format message for saving version"""

    return ' - Save version ' + version(version_name) + '\n' + get_path(yml)


def save_version_exists_error(version_name, yml):
    """Format error message previous existing saved version"""

    output_1 = colored(' - Error: Version ', 'red') + version(version_name)
    output_2 = colored(' already exists\n', 'red') + yaml_file(yml)
    return output_1 + output_2


def skip_project_message():
    """Return skip project message"""

    return ' - Skip project'


def type_error(name, yml, type_name):
    """Return formatted error string for value with wrong type"""

    output_1 = yaml_path(yml) + colored(' - Error: ', 'red') + colored(name, attrs=['bold'])
    output_2 = colored(' type should be ', 'red') + colored(type_name, 'yellow')
    return output_1 + output_2


def unknown_entry_error(name, collection, yml):
    """Return formatted error string for unknown entry in collection"""

    if len(collection) > 1:
        output_1 = yaml_path(yml) + colored(' - Error: Unknown entries in ', 'red')
    else:
        output_1 = yaml_path(yml) + colored(' - Error: Unknown entry in ', 'red')
    dict_entries = ''.join('{}: {}\n'.format(key, val) for key, val in sorted(collection.items())).rstrip()
    output_2 = colored('\n\n' + str(dict_entries), attrs=['bold'])
    return output_1 + colored(name, attrs=['bold']) + output_2


def version(version_name):
    """Return formatted string for clowder.yaml version"""

    return colored(version_name, attrs=['bold'])


def yaml_path(yml):
    """Returns formatted yaml path"""

    return get_path(symlink_target(yml)) + '\n'


def yaml_file(yml):
    """Return formatted string for clowder.yaml file"""

    return colored(yml, 'cyan')


def yaml_string(yaml_output):
    """Return yaml string from python data structures"""

    try:
        return yaml.safe_dump(yaml_output, default_flow_style=False, indent=4)
    except yaml.YAMLError:
        cprint('Failed to dump yaml', 'red')
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
