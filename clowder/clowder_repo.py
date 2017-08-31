"""Clowder repo management"""
import atexit
import os
import shutil
import subprocess
import sys
from termcolor import colored
from clowder.utility.git_utilities import (
    git_add,
    git_branches,
    git_checkout,
    git_commit,
    git_create_repo,
    git_fetch,
    git_is_dirty,
    git_pull,
    git_push,
    git_reset_head,
    git_status
)
from clowder.utility.clowder_utilities import (
    force_symlink,
    format_project_string,
    format_ref_string,
    print_validation,
    remove_prefix,
    validate_repo_state
)
from clowder.utility.repeated_timer import RepeatedTimer

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
        repo_branch = 'refs/heads/' + branch
        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)
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
            path_output = colored('.clowder/clowder.yaml', 'cyan')
        else:
            relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
            path_output = colored(relative_path, 'cyan')
            yaml_file = os.path.join(self.root_directory, relative_path)

        if os.path.isfile(yaml_file):
            yaml_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            print(' - Symlink ' + path_output)
            force_symlink(yaml_file, yaml_symlink)
        else:
            print(path_output + " doesn't seem to exist")
            print('')
            sys.exit(1)

    def print_status(self):
        """Print clowder repo status"""
        repo_path = os.path.join(self.root_directory, '.clowder')
        # FIXME: Probably should remove this as it assumes .clowder repo which isn't git directory
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            output = colored('.clowder', 'green')
            print(output)
            return
        print(' - Fetching upstream changes for clowder repo', end="", flush=True)
        timer = RepeatedTimer(1, _print_progress)
        git_fetch(self.clowder_path)
        timer.stop()
        print("\n")
        project_output = format_project_string(repo_path, '.clowder')
        current_ref_output = format_ref_string(repo_path)

        clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.islink(clowder_symlink):
            real_path = os.path.realpath(clowder_symlink)
            clowder_path = remove_prefix(real_path + '/', self.root_directory)
            path_output = colored(clowder_path[1:-1], 'cyan')
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
        command_output = colored('$ ' + command, attrs=['bold'])
        print(command_output)
        subprocess.call(command.split(), cwd=self.clowder_path)

    def status(self):
        """Print clowder repo git status"""
        git_status(self.clowder_path)

    def _validate(self):
        """Validate status of clowder repo"""
        if not validate_repo_state(self.clowder_path):
            print_validation(self.clowder_path)
            print('')
            sys.exit(1)

def _print_progress():
    print('.', end="", flush=True)
