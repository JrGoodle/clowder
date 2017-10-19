"""Clowder repo management"""

from __future__ import print_function

import atexit
import os
import sys

from git import GitError
from termcolor import colored, cprint

from clowder.utility.clowder_utilities import (
    execute_command,
    existing_git_repository,
    force_symlink,
    is_offline,
    remove_directory
)
from clowder.utility.git.printing import (
    format_project_string,
    format_project_ref_string,
    print_git_status,
    print_validation
)
from clowder.utility.git.git_repo import GitRepo
from clowder.utility.printing import (
    format_command,
    format_path,
    format_command_failed_error,
    print_error,
    remove_prefix
)


class ClowderRepo(object):
    """Class encapsulating clowder repo information"""

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.clowder_path = os.path.join(self.root_directory, '.clowder')

    def add(self, files):
        """Add files in clowder repo to git index"""
        clowder = GitRepo(self.clowder_path)
        try:
            print(' - Add files to git index')
            print(clowder.repo.git.add(files))
        except GitError as err:
            cprint(' - Failed to add files to git index', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        print_git_status(self.clowder_path)

    def branches(self):
        """Return current local branches"""
        clowder = GitRepo(self.clowder_path)
        return clowder.print_branches(local=True, remote=True)

    def checkout(self, ref):
        """Checkout ref in clowder repo"""
        clowder = GitRepo(self.clowder_path)
        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            print_git_status(self.clowder_path)
        else:
            clowder.checkout(ref)

    def clean(self):
        """Discard changes in clowder repo"""
        clowder = GitRepo(self.clowder_path)
        if self.is_dirty():
            print(' - Discard current changes')
            clowder.clean(args='fdx')
        else:
            print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo"""
        clowder = GitRepo(self.clowder_path)
        try:
            print(' - Commit current changes')
            print(clowder.repo.git.commit(message=message))
        except GitError as err:
            cprint(' - Failed to commit current changes', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def init(self, url, branch):
        """Clone clowder repo from url"""
        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)
        clowder = GitRepo(self.clowder_path)
        clowder.create_clowder_repo(url, 'origin', branch)
        self.link()

    def init_exit_handler(self):
        """Exit handler for deleting files if init fails"""
        if os.path.isdir(self.clowder_path):
            clowder_yaml = os.path.join(self.root_directory, 'clowder.yaml')
            if not os.path.isfile(clowder_yaml):
                remove_directory(self.clowder_path)
                sys.exit(1)

    def is_dirty(self):
        """Check if project is dirty"""
        clowder = GitRepo(self.clowder_path)
        return clowder.is_dirty()

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
        if not existing_git_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return
        if not is_offline() and fetch:
            print(' - Fetch upstream changes for clowder repo')
            clowder = GitRepo(self.clowder_path)
            clowder.fetch('origin')
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
        clowder = GitRepo(self.clowder_path)
        if clowder.repo.head.is_detached:
            print(' - HEAD is detached')
            return
        try:
            print(' - Pull latest changes')
            print(clowder.repo.git.pull())
        except GitError as err:
            cprint(' - Failed to pull latest changes', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def push(self):
        """Push clowder repo changes"""
        clowder = GitRepo(self.clowder_path)
        if clowder.repo.head.is_detached:
            print(' - HEAD is detached')
            return
        try:
            print(' - Push local changes')
            print(clowder.repo.git.push())
        except GitError as err:
            cprint(' - Failed to push local changes', 'red')
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    def run_command(self, command):
        """Run command in clowder repo"""
        print(format_command(command))
        return_code = execute_command(command.split(), self.clowder_path)
        if return_code != 0:
            print(format_command_failed_error(command))
            sys.exit(return_code)

    def git_status(self):
        """Print clowder repo git status"""
        print_git_status(self.clowder_path)

    def _validate_groups(self):
        """Validate status of clowder repo"""
        clowder = GitRepo(self.clowder_path)
        if not clowder.validate_repo():
            print_validation(self.clowder_path)
            print()
            sys.exit(1)
