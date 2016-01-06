"""Representation of clowder.yaml fork"""
import os
from termcolor import cprint
from clowder.utility.clowder_utilities import (
    format_project_string,
    format_ref_string
)
from clowder.utility.git_utilities import (
    git_create_remote,
    git_fetch
)

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, name, path, source, remote, depth):
        self.name = name
        self.path = path
        self.remote = remote
        self.depth = depth
        self.url = source.get_url_prefix() + self.name + ".git"

    def herd(self):
        """Herd remote data from fork"""
        self._print_status()
        git_create_remote(self.path, self.remote, self.url)
        git_fetch(self.path, self.remote, self.depth)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote}

    def _print_status(self):
        """Print formatted fork status"""
        if not os.path.isdir(os.path.join(self.path, '.git')):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(self.path, self.name)
        current_ref_output = format_ref_string(self.path)
        print(project_output + ' ' + current_ref_output)
