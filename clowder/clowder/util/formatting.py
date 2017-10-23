"""String formatting utilities"""

import os
import sys

import yaml
from termcolor import colored, cprint


def clowder_command(cmd):
    """Return formatted clowder command name"""
    return colored(cmd, attrs=['bold'])


def command(cmd):
    """Return formatted command name"""
    if isinstance(cmd, list):
        command_output = " ".join(cmd)
    else:
        command_output = cmd
    return colored('$ ' + command_output, attrs=['bold'])


def command_failed_error(cmd):
    """Format error message for failed command"""
    output_1 = colored(' - Error: Failed to run command ', 'red')
    output_2 = command(cmd)
    return output_1 + output_2 + '\n'


def depth_error(depth, yml):
    """Return formatted error string for invalid depth"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored('depth', attrs=['bold'])
    output_4 = colored(' must be a positive integer\n', 'red')
    output_5 = colored('depth: ' + str(depth), attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5


def empty_yaml_error(yml):
    """Return formatted error string for empty clowder.yaml"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: No entries in ', 'red')
    output_3 = yml('clowder.yaml')
    return output_1 + output_2 + output_3


def error(err):
    """Return error message for generic error"""
    return str(err) + '\n'


def file_exists_error(pth):
    """Format error message for already existing file"""
    output_1 = colored(' - Error: File already exists\n', 'red')
    output_2 = path(pth)
    return output_1 + output_2


def fork_string(name):
    """Return formatted fork name"""
    return colored(name, 'cyan')


def invalid_entries_error(name, collection, yml):
    """Return formatted error string for invalid entry in collection"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: No entries in ', 'red')
    output_3 = colored(name, attrs=['bold'])
    empty_output = output_1 + output_2 + output_3

    if isinstance(collection, list):
        return empty_output

    dict_entries = ''.join('{}: {}\n'.format(key, val)
                           for key, val in sorted(collection.items())).rstrip()
    length = len(collection)
    if length is 0:
        return empty_output
    elif length > 1:
        output_2 = colored(' - Error: Unknown entries in ', 'red')
    else:
        output_2 = colored(' - Error: Unknown entry in ', 'red')
    output_3 = colored(name + '\n\n' + str(dict_entries), attrs=['bold'])
    return output_1 + output_2 + output_3


def invalid_ref_error(ref, yml):
    """Return formatted error string for incorrect ref"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored('ref', attrs=['bold'])
    output_4 = colored(' value ', 'red')
    output_5 = colored(ref, attrs=['bold'])
    output_6 = colored(' is not formatted correctly', 'red')
    return output_1 + output_2 + output_3 + output_4 + output_5 + output_6


def invalid_yaml_error():
    """Return error message for invalid clowder.yaml"""
    clowder_output = yaml_file('clowder.yaml')
    return '\n' + clowder_output + ' appears to be invalid'


def missing_entry_error(entry, name, yml):
    """Return formatted error string for missing entry in dictionary"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: Missing ', 'red')
    output_3 = colored(str(entry), attrs=['bold'])
    output_4 = colored(' in ', 'red')
    output_5 = colored(str(name), attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5


def missing_imported_yaml_error(pth, yml):
    """Return formatted error string for missing imported clowder.yaml"""
    yml = symlink_target(yml)
    output_1 = pth(yml) + '\n'
    output_2 = colored(' - Error: Missing imported file\n', 'red')
    output_3 = path(pth)
    return output_1 + output_2 + output_3


def missing_yaml_error():
    """Format error message for missing clowder.yaml"""
    clowder_output = yaml_file('clowder.yaml')
    return clowder_output + ' appears to be missing'


def not_list_error(name, yml):
    """Return formatted error string for value that's not a list"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('list', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def not_dictionary_error(name, yml):
    """Return formatted error string for value that's not a dictionary"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('dict', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def not_string_error(name, yml):
    """Return formatted error string for value that's not a string"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('str', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def not_bool_error(name, yml):
    """Return formatted error string for value that's not a boolean"""
    yml = symlink_target(yml)
    output_1 = path(yml) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('bool', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def offline_error():
    """Return error message for no internet connection"""
    colored('No available internet connection\n', 'red')


def open_file_error(pth):
    """Format error message for failing to open file"""
    output_1 = colored(' - Error: Failed to open file\n', 'red')
    output_2 = path(pth)
    return output_1 + output_2


def parallel_exception_error(pth, *args):
    """Return formatted error string for parallel error"""
    return path(pth) + '\n' + ''.join(args)


def path(pth):
    """Return formatted path"""
    return colored(pth, 'cyan')


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
    message_1 = colored(' - Remote ', 'red')
    remote_output = remote_string(remote_name)
    message_2 = colored(' already exists with a different url', 'red')
    actual_url_output = path(actual_url)
    remote_url_output = path(remote_url)
    return message_1 + remote_output + message_2 + '\n' + actual_url_output + ' should be ' + remote_url_output + '\n'


def remote_name_error(fork, project, remote):
    """Return formatted error string for fork with same remote as project"""
    # yaml_file = symlink_target(yaml_file)
    # output_1 = path(yaml_file) + '\n'
    output_1 = colored(' - Error: fork ', 'red')
    output_2 = colored(fork, attrs=['bold'])
    output_3 = colored(' and project ', 'red')
    output_4 = colored(project, attrs=['bold'])
    output_5 = colored(' have same remote name ', 'red')
    output_6 = colored(remote, attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5 + output_6


def remote_string(remote):
    """Return formatted remote name"""
    return colored(remote, 'yellow')


# http://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    """Remove prefix from a string"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def save_file_error(pth):
    """Format error message for failing to save file"""
    output_1 = colored(' - Error: Failed to save file\n', 'red')
    output_2 = path(pth)
    return output_1 + output_2


def save_version(version_name, yml):
    """Format message for saving version"""
    output_1 = version(version_name)
    output_2 = path(yml)
    return ' - Save version ' + output_1 + '\n' + output_2


def save_version_exists_error(version_name, yml):
    """Format error message previous existing saved version"""
    output_1 = colored(' - Error: Version ', 'red')
    output_2 = version(version_name)
    output_3 = colored(' already exists\n', 'red')
    output_4 = yaml_file(yml)
    return output_1 + output_2 + output_3 + output_4


def skip_project_message():
    """Return skip project message"""
    return ' - Skip project'


def symlink_target(pth):
    """Returns target path if input is a symlink"""
    if os.path.islink(pth):
        return os.readlink(pth)
    return pth


def version(version_name):
    """Return formatted string for clowder.yaml version"""
    return colored(version_name, attrs=['bold'])


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
