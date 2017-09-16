"""String format and printing utilities"""
from termcolor import colored

def format_command(command):
    """Return formatted command name"""
    return colored('$ ' + command, attrs=['bold'])

def format_ref_string(ref):
    """Return formatted ref name"""
    return colored('(' + ref + ')', 'magenta')

def format_remote_string(remote):
    """Return formatted remote name"""
    return colored(remote, 'yellow')

def print_error(error):
    """Return formatted ref name"""
    message = colored(' - Error: ', 'red')
    print(message + str(error))
    print()

# http://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    """Remove prefix from a string"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
