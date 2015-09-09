"""Clowder repo management"""
import emoji, os
from termcolor import colored
from clowder.utility.git_utilities import (
    git_clone_url_at_path,
    git_is_detached,
    git_pull
)
from clowder.utility.clowder_utilities import (
    format_project_string,
    format_ref_string,
    print_exiting,
    print_validation,
    validate_repo_state
)

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, 'clowder')

    def breed(self, url):
        """Clone clowder repo from url"""
        git_clone_url_at_path(url, self.clowder_path, 'refs/heads/master', 'origin')
        self.symlink_yaml()

    def print_status(self):
        """Print clowder repo status"""
        repo_path = os.path.join(self.root_directory, 'clowder')
        cat_face = emoji.emojize(':cat:', use_aliases=True)
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            output = colored('clowder', 'green')
            print(cat_face + '  ' + output)
            return
        project_output = format_project_string(repo_path, 'clowder')
        current_ref_output = format_ref_string(repo_path)
        print(cat_face + '  ' + project_output + ' ' + current_ref_output)

    def symlink_yaml(self, version=None):
        """Create symlink pointing to clowder.yaml file"""
        if version == None:
            yaml_file = os.path.join(self.root_directory, 'clowder', 'clowder.yaml')
            path_output = colored('clowder/clowder.yaml', 'cyan')
        else:
            relative_path = os.path.join('clowder', 'versions', version, 'clowder.yaml')
            path_output = colored(relative_path, 'cyan')
            yaml_file = os.path.join(self.root_directory, relative_path)
        os.chdir(self.root_directory)
        if os.path.isfile(yaml_file):
            if os.path.isfile('clowder.yaml'):
                os.remove('clowder.yaml')
            print(' - Symlink ' + path_output)
            os.symlink(yaml_file, 'clowder.yaml')
        else:
            print(path_output + " doesn't seem to exist")
            print_exiting()

    def sync(self):
        """Sync clowder repo"""
        self._validate()
        if not git_is_detached(self.clowder_path):
            print(' - Pulling latest changes')
            git_pull(self.clowder_path)
        self.symlink_yaml()

    def _validate(self):
        """Validate status of clowder repo"""
        if not validate_repo_state(self.clowder_path):
            print_validation(self.clowder_path)
            print_exiting()
