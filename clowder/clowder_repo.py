"""Clowder repo management"""
import atexit
import os
import shutil
import sys
from termcolor import colored
from clowder.utility.git_utilities import (
    git_add,
    git_branches,
    git_checkout,
    git_commit,
    git_create_repo,
    git_existing_repository,
    git_fetch_silent,
    git_is_dirty,
    git_pull,
    git_push,
    git_reset_head,
    git_status,
    git_validate_repo_state
)
from clowder.utility.clowder_utilities import (
    execute_command,
    force_symlink
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
        git_add(self.clowder_path, files)
        git_status(self.clowder_path)

    def branches(self):
        """Return current local branches"""
        return git_branches(self.clowder_path)

    def checkout(self, ref):
        """Checkout ref in clowder repo"""
        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
        else:
            git_checkout(self.clowder_path, ref)

    def clean(self):
        """Discard changes in clowder repo"""
        if self.is_dirty():
            print(' - Discard current changes')
            git_reset_head(self.clowder_path)
        else:
            print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo"""
        git_commit(self.clowder_path, message)

    def init(self, url, branch):
        """Clone clowder repo from url"""
        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)
        repo_branch = 'refs/heads/' + branch
        git_create_repo(url, self.clowder_path, 'origin', repo_branch)
        self.link()

    def init_exit_handler(self):
        """Exit handler for deleting files if init fails"""
        if os.path.isdir(self.clowder_path):
            clowder_yaml = os.path.join(self.root_directory, 'clowder.yaml')
            if not os.path.isfile(clowder_yaml):
                shutil.rmtree(self.clowder_path)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.clowder_path)

    def link(self, version=None):
        """Create symlink pointing to clowder.yaml file"""
        if version is None:
            yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            path_output = format_path('.clowder/clowder.yaml')
        else:
            relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
            path_output = format_path(relative_path)
            yaml_file = os.path.join(self.root_directory, relative_path)

        if os.path.isfile(yaml_file):
            yaml_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            print(' - Symlink ' + path_output)
            force_symlink(yaml_file, yaml_symlink)
        else:
            print(path_output + " doesn't seem to exist")
            print()
            sys.exit(1)

    def print_status(self):
        """Print clowder repo status"""
        repo_path = os.path.join(self.root_directory, '.clowder')
        if not git_existing_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return
        print(' - Fetch upstream changes for clowder repo')
        git_fetch_silent(self.clowder_path)
        print()
        project_output = format_project_string(repo_path, '.clowder')
        current_ref_output = format_project_ref_string(repo_path)

        clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.islink(clowder_symlink):
            real_path = os.path.realpath(clowder_symlink)
            clowder_path = remove_prefix(real_path + '/', self.root_directory)
            path_output = format_path(clowder_path[1:-1])
            print(project_output + ' ' + current_ref_output + ' ~~> ' + path_output)
        else:
            print(project_output + ' ' + current_ref_output)

    def pull(self):
        """Pull clowder repo upstream changes"""
        git_pull(self.clowder_path)

    def push(self):
        """Push clowder repo changes"""
        git_push(self.clowder_path)

    def run_command(self, command):
        """Run command in clowder repo"""
        print(format_command(command))
        return_code = execute_command(command.split(), self.clowder_path)
        if return_code != 0:
            print_command_failed_error(command)
            sys.exit(return_code)

    def status(self):
        """Print clowder repo git status"""
        git_status(self.clowder_path)

    def _validate_groups(self):
        """Validate status of clowder repo"""
        if not git_validate_repo_state(self.clowder_path):
            print_validation(self.clowder_path)
            print()
            sys.exit(1)
