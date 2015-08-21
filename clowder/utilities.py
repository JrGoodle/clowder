"""Utilities for clowder"""
import os

def process_output(line):
    """Utility function for command output callbacks"""
    stripped_line = str(line).rstrip('\n')
    print(stripped_line)

def symlink_clowder_yaml(root_directory, clowder_yaml):
    """Create clowder.yaml symlink in directory pointing to file"""
    os.chdir(root_directory)
    if os.path.isfile(clowder_yaml):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowder_yaml, 'clowder.yaml')
    else:
        print(clowder_yaml + " doesn't seem to exist")
