"""Clowder repo management"""
import os
from termcolor import cprint
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_herd,
    git_validate_repo_state
)

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.clowder_path = os.path.join(self.root_directory, 'clowder')

    def clone(self, url):
        """Clone clowder repo from url"""
        cprint('clowder', 'green')
        git_clone_url_at_path(url, self.clowder_path)

    def herd(self):
        """Herd clowder repo"""
        cprint('clowder', 'green')
        git_validate_repo_state(self.clowder_path)
        git_herd(self.clowder_path, 'refs/heads/master')
