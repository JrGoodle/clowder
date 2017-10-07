"""Clowder repo management"""
import atexit
import os
import sys
from termcolor import colored
from clowder.utility.git_utilities import Git
from clowder.utility.clowder_utilities import (
    execute_command,
    existing_git_repository,
    force_symlink,
    is_offline,
    remove_directory_exit
)
from clowder.utility.print_utilities import (
    format_command,
    format_path,
    print_command_failed_error,
    remove_prefix
)
from clowder.utility.git_print_utilities import (
    format_project_string,
    format_project_ref_string,
    print_validation
)

# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, '.clowder')

    def add(self, files):
        """Add files in clowder repo to git index"""
        repo = Git(self.clowder_path)
        repo.add(files)
        repo.status()

    def branches(self):
        """Return current local branches"""
        repo = Git(self.clowder_path)
        return repo.branches()

    def checkout(self, ref):
        """Checkout ref in clowder repo"""
        repo = Git(self.clowder_path)
        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            repo.status()
        else:
            repo.checkout(ref)

    def clean(self):
        """Discard changes in clowder repo"""
        repo = Git(self.clowder_path)
        if self.is_dirty():
            print(' - Discard current changes')
            repo.reset_head()
        else:
            print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo"""
        repo = Git(self.clowder_path)
        repo.commit(message)

    def init(self, url, branch):
        """Clone clowder repo from url"""
        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)
        repo_branch = 'refs/heads/' + branch
        repo = Git(self.clowder_path)
        repo.create_repo(url, 'origin', repo_branch)
        self.link()

    def init_exit_handler(self):
        """Exit handler for deleting files if init fails"""
        if os.path.isdir(self.clowder_path):
            clowder_yaml = os.path.join(self.root_directory, 'clowder.yaml')
            if not os.path.isfile(clowder_yaml):
                remove_directory_exit(self.clowder_path)

    def is_dirty(self):
        """Check if project is dirty"""
        repo = Git(self.clowder_path)
        return repo.is_dirty(self.clowder_path)

    def link(self, version=None):
        """Create symlink pointing to clowder.yaml file"""
        if version is None:
            yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            path_output = format_path('.clowder/clowder.yaml')
        else:
            relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
            path_output = format_path(relative_path)
            yaml_file = os.path.join(self.root_directory, relative_path)

        if not os.path.isfile(yaml_file):
            print(path_output + " doesn't seem to exist\n")
            sys.exit(1)
        yaml_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        print(' - Symlink ' + path_output)
        force_symlink(yaml_file, yaml_symlink)

    def print_status(self, fetch=False):
        """Print clowder repo status"""
        repo_path = os.path.join(self.root_directory, '.clowder')
        repo = Git(self.clowder_path)
        if not existing_git_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return
        if not is_offline() and fetch:
            print(' - Fetch upstream changes for clowder repo')
            repo.fetch_silent()
        project_output = format_project_string(repo_path, '.clowder')
        current_ref_output = format_project_ref_string(repo_path)

        clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        if not os.path.islink(clowder_symlink):
            print(project_output + ' ' + current_ref_output)
            return
        real_path = os.path.realpath(clowder_symlink)
        symlink_output = format_path('clowder.yaml')
        clowder_path = remove_prefix(real_path + '/', self.root_directory)
        path_output = format_path(clowder_path[1:-1])
        print(project_output + ' ' + current_ref_output)
        print(symlink_output + ' -> ' + path_output)
        print()

    def pull(self):
        """Pull clowder repo upstream changes"""
        repo = Git(self.clowder_path)
        repo.pull()

    def push(self):
        """Push clowder repo changes"""
        repo = Git(self.clowder_path)
        repo.push()

    def run_command(self, command):
        """Run command in clowder repo"""
        print(format_command(command))
        return_code = execute_command(command.split(), self.clowder_path)
        if return_code != 0:
            print_command_failed_error(command)
            sys.exit(return_code)

    def status(self):
        """Print clowder repo git status"""
        repo = Git(self.clowder_path)
        repo.status()

    def _validate_groups(self):
        """Validate status of clowder repo"""
        repo = Git(self.clowder_path)
        if not repo.validate_repo():
            print_validation(self.clowder_path)
            print()
            sys.exit(1)
