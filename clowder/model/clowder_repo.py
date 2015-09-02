"""Clowder repo management"""
import os
from clowder.utility.print_utilities import (
    print_clowder_repo_status,
    print_exiting,
    print_validation
)
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_sync,
    git_validate_repo_state
)

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, 'clowder')

    def breed(self, url):
        """Clone clowder repo from url"""
        print_clowder_repo_status(self.root_directory)
        git_clone_url_at_path(url, self.clowder_path, 'origin')
        self.symlink_yaml()

    def sync(self):
        """Sync clowder repo"""
        self._validate()
        print_clowder_repo_status(self.root_directory)
        git_sync(self.clowder_path)
        self.symlink_yaml()

    def symlink_yaml(self, version=None):
        """Create symlink pointing to clowder.yaml file"""
        if version == None:
            yaml_file = os.path.join(self.root_directory, 'clowder', 'clowder.yaml')
        else:
            yaml_file = os.path.join(self.root_directory, 'clowder', 'versions',
                                     version, 'clowder.yaml')
        os.chdir(self.root_directory)
        if os.path.isfile(yaml_file):
            if os.path.isfile('clowder.yaml'):
                os.remove('clowder.yaml')
            os.symlink(yaml_file, 'clowder.yaml')
        else:
            print(yaml_file + " doesn't seem to exist")

    def _validate(self):
        """Validate status of clowder repo"""
        if not git_validate_repo_state(self.clowder_path):
            print_clowder_repo_status(self.root_directory)
            print_validation(self.clowder_path)
            print_exiting()
