"""Representation of clowder.yaml fork"""
from termcolor import cprint
from clowder.utility.git_print_utilities import (
    format_project_string
)
from clowder.utility.git_utilities import git_existing_repository
from clowder.utility.print_utilities import format_fork_string

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, fork, path, source):
        self.path = path
        self.name = fork['name']
        self.remote_name = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote_name}

    def print_status(self):
        """Print formatted fork status"""
        if not git_existing_repository(self.path):
            cprint(self.path, 'green')
            return
        project_output = format_project_string(self.path, self.path)
        fork_output = format_fork_string(self.name)
        print(project_output + ' ' + fork_output)
