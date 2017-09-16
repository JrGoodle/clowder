"""Representation of clowder.yaml fork"""
from termcolor import cprint
from clowder.utility.git_print_utilities import (
    format_project_string,
    format_project_ref_string
)
from clowder.utility.git_utilities import (
    git_create_remote,
    git_existing_repository,
    git_fetch_remote_ref
)

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, fork, path, source):
        self.path = path
        self.name = fork['name']
        self.remote = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def herd(self, ref, depth):
        """Herd remote data from fork"""
        self._print_status()
        git_create_remote(self.path, self.remote, self.url)
        git_fetch_remote_ref(self.path, self.remote, ref, depth)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote}

    def _print_status(self):
        """Print formatted fork status"""
        if not git_existing_repository(self.path):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(self.path, self.name)
        current_ref_output = format_project_ref_string(self.path)
        print(project_output + ' ' + current_ref_output)
