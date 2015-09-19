"""Clowder repo management"""
import emoji, os
from git import Repo
from termcolor import colored
from clowder.utility.git_utilities import (
    git_branches,
    git_clone_url_at_path,
    git_is_detached,
    git_pull
)
from clowder.utility.clowder_utilities import (
    force_symlink,
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

    def branches(self):
        """Return current local branches"""
        return git_branches(self.clowder_path)

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

        if os.path.isfile(yaml_file):
            yaml_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            print(' - Symlink ' + path_output)
            force_symlink(yaml_file, yaml_symlink)
        else:
            print(path_output + " doesn't seem to exist")
            print_exiting()

    def sync(self):
        """Sync clowder repo"""
        self._validate()
        self.print_status()
        if not git_is_detached(self.clowder_path):
            git_pull(self.clowder_path)
            self.symlink_yaml()
        else:
            print(' - HEAD is detached')
            print_exiting()

    # Disable errors shown by pylint for no specified exception types
    # pylint: disable=W0702
    def sync_branch(self, branch):
        """Sync clowder repo to specified branch"""
        try:
            repo = Repo(self.clowder_path)
        except:
            repo_path_output = colored(self.clowder_path, 'cyan')
            print("Failed to create Repo instance for " + repo_path_output)
        else:
            detached = git_is_detached(self.clowder_path)
            correct_branch = repo.active_branch.name == branch
            if detached or not correct_branch:
                try:
                    repo.git.checkout(branch)
                except:
                    print("Failed to checkout branch " + branch)
                    print_exiting()
            self._validate()
            self.print_status()
            git_pull(self.clowder_path)
            self.symlink_yaml()

    def _validate(self):
        """Validate status of clowder repo"""
        if not validate_repo_state(self.clowder_path):
            print_validation(self.clowder_path)
            print_exiting()
