# -*- coding: utf-8 -*-
"""Clowder repo class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import atexit
import os
import sys

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.git.project_repo import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_project_ref_string,
    format_project_string,
    print_validation
)
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import (
    force_symlink,
    remove_directory
)
from clowder.yaml.validating import validate_yaml


class ClowderRepo(object):
    """Class encapsulating clowder repo information

    :ivar str root_directory: Root directory of clowder projects
    :ivar str default_ref: Default ref
    :ivar str remote: Remote name
    :ivar str clowder_path: Absolute path to clowder repo
    """

    def __init__(self, root_directory):
        """ClowderController __init__

        :param str root_directory: Root directory of clowder projects
        """

        self.root_directory = root_directory
        self.default_ref = 'refs/heads/master'
        self.remote = 'origin'
        self.clowder_path = os.path.join(self.root_directory, '.clowder')
        self.repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)

        # Create clowder.yaml symlink if .clowder dir and yaml file exist
        clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.isdir(self.clowder_path):
            if not os.path.islink(clowder_symlink):
                self.link()

        self.is_yaml_valid = False
        self.error = None
        if os.path.islink(clowder_symlink):
            try:
                validate_yaml(os.path.join(self.root_directory, 'clowder.yaml'), self.root_directory)
            except ClowderError as err:
                self.error = err
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
            else:
                self.is_yaml_valid = True

    def add(self, files):
        """Add files in clowder repo to git index

        :param str files: Files to git add
        """

        self.repo.add(files)

    def branches(self):
        """Print current local branches"""

        self.repo.print_branches(local=True, remote=True)

    def checkout(self, ref):
        """Checkout ref in clowder repo

        :param str ref: Ref to git checkout
        """

        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            self.repo.status_verbose()
            return
        self.repo.checkout(ref)

    def clean(self):
        """Discard changes in clowder repo

        Equivalent to: ``git clean -ffdx``
        """

        if self.is_dirty():
            print(' - Discard current changes')
            self.repo.clean(args='fdx')
            return

        print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo

        :param str message: Git commit message
        """

        self.repo.commit(message)

    def git_status(self):
        """Print clowder repo git status

        Equivalent to: ``git status -vv``
        """

        self.repo.status_verbose()

    def init(self, url, branch):
        """Clone clowder repo from url

        :param str url: URL of repo to clone
        :param str branch: Branch to checkout
        """

        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)

        self.repo.create_clowder_repo(url, branch)
        self.link()

    def init_exit_handler(self):
        """Exit handler for deleting files if init fails"""

        if os.path.isdir(self.clowder_path):
            clowder_yaml = os.path.join(self.root_directory, 'clowder.yaml')
            if not os.path.isfile(clowder_yaml):
                remove_directory(self.clowder_path)
                sys.exit(1)

    def is_dirty(self):
        """Check if project is dirty

        :return: True, if repo is dirty
        :rtype: bool
        """

        return self.repo.is_dirty()

    def link(self, version=None):
        """Create symlink pointing to clowder.yaml file

        .. py:function:: link(version=None)

        :param Optional[str] version: Version name of clowder.yaml to link
        """

        if version is None:
            yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            path_output = fmt.get_path('.clowder/clowder.yaml')
        else:
            relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
            path_output = fmt.get_path(relative_path)
            yaml_file = os.path.join(self.root_directory, relative_path)

        if not os.path.isfile(yaml_file):
            print(path_output + " doesn't seem to exist\n")
            sys.exit(1)

        yaml_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        print(' - Symlink ' + path_output)
        force_symlink(yaml_file, yaml_symlink)

    def print_status(self, fetch=False):
        """Print clowder repo status

        .. py:function:: print_status(fetch=False)

        :param Optional[str] fetch: Fetch before printing status
        """

        repo_path = os.path.join(self.root_directory, '.clowder')
        if not existing_git_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return

        if not is_offline() and fetch:
            print(' - Fetch upstream changes for clowder repo')
            self.repo.fetch(self.remote)

        project_output = format_project_string(self.repo, '.clowder')
        current_ref_output = format_project_ref_string(self.repo)

        clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
        if not os.path.islink(clowder_symlink):
            print(project_output + ' ' + current_ref_output)
            return

        real_path = os.path.realpath(clowder_symlink)
        symlink_output = fmt.get_path('clowder.yaml')
        clowder_path = fmt.remove_prefix(real_path + '/', self.root_directory)
        path_output = fmt.get_path(clowder_path[1:-1])
        print(project_output + ' ' + current_ref_output)
        print(symlink_output + ' -> ' + path_output + '\n')

    def pull(self):
        """Pull clowder repo upstream changes"""

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).pull()

    def push(self):
        """Push clowder repo changes"""

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).push()

    def run_command(self, command):
        """Run command in clowder repo

        :param str command: Command to run
        """

        print(fmt.command(command))
        return_code = execute_command(command.split(), self.clowder_path)
        if return_code != 0:
            print(fmt.command_failed_error(command))
            sys.exit(return_code)

    def _validate_groups(self):
        """Validate status of clowder repo"""

        if not self.repo.validate_repo():
            print_validation(self.repo)
            print()
            sys.exit(1)


CLOWDER_REPO = ClowderRepo(os.getcwd())


def clowder_required(func):
    """If no clowder repo, print clowder not found message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        CLOWDER_REPO.print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        CLOWDER_REPO.print_status(fetch=True)
        return func(*args, **kwargs)

    return wrapper


def valid_clowder_yaml_required(func):
    """If clowder.yaml is invalid, print invalid yaml message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        if not CLOWDER_REPO.is_yaml_valid:
            print(fmt.invalid_yaml_error())
            print(fmt.error(CLOWDER_REPO.error))
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def _validate_clowder_repo_exists():
    """If clowder repo doesn't exist, print message and exit"""

    if not os.path.isdir(CLOWDER_REPO.clowder_path):
        cprint(' - No .clowder found in the current directory\n', 'red')
        sys.exit(1)
