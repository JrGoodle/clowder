# -*- coding: utf-8 -*-
"""Clowder repo class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import atexit
import errno
import os
import sys

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.git.project_repo import ProjectRepo
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_command
from clowder.util.file_system import remove_directory


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

    def add(self, files):
        """Add files in clowder repo to git index

        :param str files: Files to git add
        """

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).add(files)

    def branches(self):
        """Print current local branches"""

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).print_branches(local=True, remote=True)

    def checkout(self, ref):
        """Checkout ref in clowder repo

        :param str ref: Ref to git checkout
        """

        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            repo.status_verbose()
            return
        repo.checkout(ref)

    def clean(self):
        """Discard changes in clowder repo

        Equivalent to: ``git clean -ffdx``
        """

        if self.is_dirty():
            print(' - Discard current changes')
            ProjectRepo(self.clowder_path, self.remote, self.default_ref).clean(args='fdx')
            return

        print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo

        :param str message: Git commit message
        """

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).commit(message)

    def init(self, url, branch):
        """Clone clowder repo from url

        :param str url: URL of repo to clone
        :param str branch: Branch to checkout
        """

        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).create_clowder_repo(url, branch)
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

        return ProjectRepo(self.clowder_path, self.remote, self.default_ref).is_dirty()

    def link(self, version=None):
        """Create symlink pointing to clowder.yaml file

        :param Optional[str] version: Version name of clowder.yaml to link. Defaults to None for default clowder.yaml
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

        :param Optional[str] fetch: Fetch before printing status. Defaults to False
        """

        repo_path = os.path.join(self.root_directory, '.clowder')
        if not ProjectRepo.existing_git_repository(repo_path):
            output = colored('.clowder', 'green')
            print(output)
            return

        if not is_offline() and fetch:
            print(' - Fetch upstream changes for clowder repo')
            repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
            repo.fetch(self.remote)

        project_output = ProjectRepo.format_project_string(repo_path, '.clowder')
        current_ref_output = ProjectRepo.format_project_ref_string(repo_path)

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

    def git_status(self):
        """Print clowder repo git status

        Equivalent to: ``git status -vv``
        """

        ProjectRepo(self.clowder_path, self.remote, self.default_ref).status_verbose()

    def _validate_groups(self):
        """Validate status of clowder repo"""

        if not ProjectRepo(self.clowder_path, self.remote, self.default_ref).validate_repo():
            ProjectRepo.print_validation(self.clowder_path)
            print()
            sys.exit(1)


def force_symlink(file1, file2):
    """Force symlink creation

    :param str file1: File to create symlink pointing to
    :param str file2: Symlink location
    """

    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)
    except (KeyboardInterrupt, SystemExit):
        os.remove(file2)
        os.symlink(file1, file2)
        sys.exit(1)
