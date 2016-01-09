"""Clowder repo management"""
import os
import subprocess
import sys
import emoji
from termcolor import colored
from clowder.utility.git_utilities import (
    git_add,
    git_branches,
    git_create_repo,
    git_is_dirty,
    git_reset_head,
    git_status
)
from clowder.utility.clowder_utilities import (
    force_symlink,
    format_project_string,
    format_ref_string,
    print_validation,
    validate_repo_state
)

class ClowderRepo(object):
    """Class encapsulating clowder repo information"""
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, '.clowder')

    def add(self, files):
        """Add files in clowder repo to git"""
        print(' - Add files in clowder repo')
        git_add(self.clowder_path, files)
        git_status(self.clowder_path)

    def branches(self):
        """Return current local branches"""
        return git_branches(self.clowder_path)

    def checkout(self, ref):
        """Checkout ref in clowder repo"""
        print('clowder repo checkout ' + ref)

    def clean(self):
        """Discard changes in clowder repo"""
        if self.is_dirty():
            print(' - Discarding current changes')
            git_reset_head(self.clowder_path)
        else:
            print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo"""
        print('clowder repo commit ' + message)

    def init(self, url, branch):
        """Clone clowder repo from url"""
        repo_branch = 'refs/heads/' + branch
        git_create_repo(url, self.clowder_path, 'origin', repo_branch)
        self.symlink_yaml()

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.clowder_path)

    def print_status(self):
        """Print clowder repo status"""
        repo_path = os.path.join(self.root_directory, '.clowder')
        cat_face = emoji.emojize(':cat:', use_aliases=True)
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            output = colored('clowder', 'green')
            print(cat_face + '  ' + output)
            return
        project_output = format_project_string(repo_path, '.clowder')
        current_ref_output = format_ref_string(repo_path)
        print(cat_face + '  ' + project_output + ' ' + current_ref_output)

    def pull(self):
        """Pull clowder repo upstream changes"""
        print('clowder repo pull')

    def push(self):
        """Push clowder repo changes"""
        print('clowder repo push')


    def run_command(self, command):
        """Run command in clowder repo"""
        command_output = colored('$ ' + command, attrs=['bold'])
        print(command_output)
        subprocess.call(command.split(), cwd=self.clowder_path)

    def status(self):
        """Print clowder repo git status"""
        git_status(self.clowder_path)

    def symlink_yaml(self, version=None):
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

    def _validate(self):
        """Validate status of clowder repo"""
        if not validate_repo_state(self.clowder_path):
            print_validation(self.clowder_path)
            print('')
            sys.exit(1)
