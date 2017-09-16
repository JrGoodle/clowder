"""String formatting and printing utilities"""
from termcolor import colored

# Disable errors shown by pylint for invalid function name
# pylint: disable=C0103

def format_clowder_command(command):
    """Return formatted clowder command name"""
    return colored(command, attrs=['bold'])

def format_command(command):
    """Return formatted command name"""
    return colored('$ ' + command, attrs=['bold'])

def format_depth_error(depth):
    """Return formatted error string for invalid depth"""
    output_1 = colored(' - ', 'red')
    output_2 = colored(' must be a positive integer', 'red')
    return output_1 + '\'depth\'' + output_2 + '\n   - depth: ' + str(depth)

def format_missing_entry_error(entry, name):
    """Return formatted error string for missing entry in dictionary"""
    output_1 = colored(' - Missing ', 'red')
    output_2 = colored(' in ', 'red')
    return output_1 + str(entry) + output_2 + name

def format_missing_imported_yaml_error(path):
    """Return formatted error string for missing imported clowder.yaml"""
    output_1 = colored(' - Missing imported ', 'red')
    output_2 = format_yaml_file('clowder.yaml')
    output_3 = colored(' at ', 'red')
    output_4 = format_path(path)
    return output_1 + output_2 + output_3 + output_4

def format_not_array_error(name):
    """Return formatted error string for no array"""
    output_1 = colored(' - ', 'red')
    output_2 = colored(' doesn\'t contain array', 'red')
    return output_1 + name + output_2

def format_path(path):
    """Return formatted path"""
    return colored(path, 'cyan')

def format_ref_string(ref):
    """Return formatted ref name"""
    return colored('(' + ref + ')', 'magenta')

def format_remote_string(remote):
    """Return formatted remote name"""
    return colored(remote, 'yellow')

def format_version(version_name):
    """Return formatted string for clowder.yaml version"""
    return colored(version_name, attrs=['bold'])

def format_unknown_entries_error(name, dictionary):
    """Return formatted error string for unknown entry in dictionary"""
    dict_entries = ''.join('   - {}: {}\n'.format(key, val)
                           for key, val in sorted(dictionary.items())).rstrip()
    length = len(dictionary)
    if length is 0:
        return colored(' - No entries', 'red')
    elif length > 1:
        unknown_entry_output = colored(' - Unknown entries in ', 'red')
    else:
        unknown_entry_output = colored(' - Unknown entry in ', 'red')
    return unknown_entry_output + name + '\n' + dict_entries

def format_yaml_file(yaml_file):
    """Return formatted string for clowder.yaml file"""
    return colored(yaml_file, 'cyan')

def print_command_failed_error(command):
    """Print error message for failed command"""
    output_1 = colored(' - Failed to run command\n   ', 'red')
    output_2 = format_command(command)
    return output_1 + output_2

def print_empty_yaml_error(yaml_file):
    """Print error message for empty clowder.yaml"""
    output_1 = colored(' - ', 'red')
    output_2 = format_yaml_file('clowder.yaml')
    output_3 = colored(' is empty ', 'red')
    return output_1 + output_2 + output_3 + yaml_file

def print_error(error):
    """Print error message for generic exception"""
    message = colored(' - Error: ', 'red')
    print(message + str(error))
    print()

def print_invalid_yaml_error():
    """Print error message for invalid clowder.yaml"""
    clowder_output = format_yaml_file('clowder.yaml')
    print(clowder_output + ' appears to be invalid')

def print_missing_yaml_error():
    """Print error message for missing clowder.yaml"""
    clowder_output = format_yaml_file('clowder.yaml')
    print(clowder_output + ' appears to be missing')

def print_recursive_import_error(depth):
    """Print error message for too many recursive imports"""
    clowder_output = format_yaml_file('clowder.yaml')
    print(clowder_output + ' has too many recursive imports')
    print('Currently the max is ' + str(depth))

def print_save_version(version_name, yaml_file):
    """Print message for saving version"""
    output_1 = format_version(version_name)
    output_2 = format_yaml_file(yaml_file)
    print(' - Save version ' + output_1 + ' at '+ output_2)

def print_save_version_exists_error(version_name, yaml_file):
    """Print error message previous existing saved version"""
    output_1 = colored(' - Version ', 'red')
    output_2 = format_version(version_name)
    output_3 = colored(' already exists at ', 'red')
    output_4 = format_yaml_file(yaml_file)
    print(output_1 + output_2 + output_3 + output_4)

# http://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    """Remove prefix from a string"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
