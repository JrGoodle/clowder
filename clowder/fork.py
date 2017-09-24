"""Representation of clowder.yaml fork"""
import os
from termcolor import cprint
from clowder.utility.git_print_utilities import (
    format_project_ref_string,
    format_project_string
)
from clowder.utility.git_utilities import git_existing_repository

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, fork, root_directory, path, source):
        self.root_directory = root_directory
        self.path = path
        self.name = fork['name']
        self.remote_name = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote_name}

    def print_status(self):
        """Print formatted fork status"""
        if not git_existing_repository(self.path):
            cprint(self.path, 'green')
            return
        project_output = format_project_string(self.path, self.path)
        current_ref_output = format_project_ref_string(self.full_path())
        print(project_output + ' ' + current_ref_output)
