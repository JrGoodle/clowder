"""Representation of clowder.yaml fork"""
import os
from termcolor import cprint
from clowder.utility.git_print_utilities import (
    format_project_string
)
from clowder.utility.git_utilities import (
    git_existing_repository,
    git_herd_branch_fork,
    git_herd_fork
)
from clowder.utility.print_utilities import format_fork_string

class Fork(object):
    """clowder.yaml fork class"""

    def __init__(self, fork, root_directory, path, source):
        self.root_directory = root_directory
        self.path = path
        self.name = fork['name']
        self.remote = fork['remote']
        self.url = source.get_url_prefix() + self.name + ".git"

    def herd(self, ref, depth, branch=None):
        """Herd remote data from fork"""
        self._print_status()
        if branch is None:
            git_herd_fork(self.path, self.url, self.remote, ref, depth)
        else:
            git_herd_branch_fork(self.path, self.url, self.remote, branch, ref, depth)

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'remote': self.remote}

    def _print_status(self):
        """Print formatted fork status"""
        if not git_existing_repository(self.path):
            cprint(self.path, 'green')
            return
        project_output = format_project_string(self.path, self.path)
        fork_output = format_fork_string(self.name)
        print(project_output + ' ' + fork_output)
