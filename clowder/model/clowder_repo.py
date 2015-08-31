"""Clowder repo management"""
import os
from clowder.utility.print_utilities import print_clowder_repo_status
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_herd_clowder,
    git_validate_repo_state
)

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, 'clowder')

    def clone(self, url):
        """Clone clowder repo from url"""
        print_clowder_repo_status(self.root_directory)
        git_clone_url_at_path(url, self.clowder_path)

    def herd(self):
        """Herd clowder repo"""
        git_validate_repo_state(self.clowder_path)
        print_clowder_repo_status(self.root_directory)
        git_herd_clowder(self.clowder_path)
