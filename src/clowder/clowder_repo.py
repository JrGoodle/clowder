# -*- coding: utf-8 -*-
"""Clowder repo class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import atexit
import os

from termcolor import colored

import clowder.util.formatting as fmt
from clowder import ROOT_DIR
from clowder.error.clowder_error import ClowderError
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.git.project_repo import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_project_ref_string,
    format_project_string,
    print_validation
)
from clowder.util.clowder_utils import link_clowder_yaml
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory
from clowder.yaml.validating import validate_yaml


class ClowderRepo(object):
    """Class encapsulating clowder repo information

    :ivar str default_ref: Default ref
    :ivar str remote: Remote name
    :ivar str clowder_path: Absolute path to clowder repo
    """

    def __init__(self):
        """ClowderController __init__

        :raise ClowderExit:
        """

        self.default_ref = 'refs/heads/master'
        self.remote = 'origin'
        self.clowder_path = os.path.join(ROOT_DIR, '.clowder')
        self.repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)

        # Create clowder.yaml symlink if .clowder dir and yaml file exist
        clowder_symlink = os.path.join(ROOT_DIR, 'clowder.yaml')
        if os.path.isdir(self.clowder_path) and not os.path.islink(clowder_symlink):
            link_clowder_yaml()

        self.error = None
        if os.path.islink(clowder_symlink):
            try:
                validate_yaml(os.path.join(ROOT_DIR, 'clowder.yaml'))
            except ClowderYAMLError as err:
                self.error = err
            except (KeyboardInterrupt, SystemExit):
                raise ClowderExit(1)

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
        link_clowder_yaml()

    def init_exit_handler(self):
        """Exit handler for deleting files if init fails

        :raise ClowderExit:
        """

        if os.path.isdir(self.clowder_path):
            clowder_yaml = os.path.join(ROOT_DIR, 'clowder.yaml')
            if not os.path.islink(clowder_yaml):
                remove_directory(self.clowder_path)
                raise ClowderExit(1)

    def is_dirty(self):
        """Check if project is dirty

        :return: True, if repo is dirty
        :rtype: bool
        """

        return self.repo.is_dirty()

    def print_status(self, fetch=False):
        """Print clowder repo status

        .. py:function:: print_status(fetch=False)

        :param Optional[str] fetch: Fetch before printing status
        """

        repo_path = os.path.join(ROOT_DIR, '.clowder')
        if not existing_git_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return

        if not is_offline() and fetch:
            print(' - Fetch upstream changes for clowder repo')
            self.repo.fetch(self.remote)

        project_output = format_project_string(self.repo, '.clowder')
        current_ref_output = format_project_ref_string(self.repo)

        clowder_symlink = os.path.join(ROOT_DIR, 'clowder.yaml')
        if not os.path.islink(clowder_symlink):
            print(project_output + ' ' + current_ref_output)
            return

        real_path = os.path.realpath(clowder_symlink)
        symlink_output = fmt.get_path('clowder.yaml')
        clowder_path = fmt.remove_prefix(real_path + '/', ROOT_DIR)
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
        :raise ClowderError:
        """

        print(fmt.command(command))
        try:
            execute_command(command.split(), self.clowder_path)
        except ClowderError as err:
            print(fmt.command_failed_error(command))
            raise err

    def _validate_groups(self):
        """Validate status of clowder repo

        :raise ClowderExit:
        """

        if not self.repo.validate_repo():
            print_validation(self.repo)
            print()
            raise ClowderExit(1)


CLOWDER_REPO = ClowderRepo()


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
