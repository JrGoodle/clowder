"""Clowder repo management"""

from __future__ import print_function

import atexit
import errno
import os
import subprocess
import sys

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.git.project_repo import ProjectRepo
from clowder.util.connectivity import is_offline
from clowder.util.file_system import remove_directory


class ClowderRepo(object):
    """Class encapsulating clowder repo information"""

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.default_ref = 'refs/heads/master'
        self.remote = 'origin'
        self.clowder_path = os.path.join(self.root_directory, '.clowder')

    def add(self, files):
        """Add files in clowder repo to git index"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.add(files)

    def branches(self):
        """Return current local branches"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        return repo.print_branches(local=True, remote=True)

    def checkout(self, ref):
        """Checkout ref in clowder repo"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        if self.is_dirty():
            print(' - Dirty repo. Please stash, commit, or discard your changes')
            repo.status_verbose()
            return
        repo.checkout(ref)

    def clean(self):
        """Discard changes in clowder repo"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        if self.is_dirty():
            print(' - Discard current changes')
            repo.clean(args='fdx')
            return
        print(' - No changes to discard')

    def commit(self, message):
        """Commit current changes in clowder repo"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.commit(message)

    def init(self, url, branch):
        """Clone clowder repo from url"""
        # Register exit handler to remove files if cloning repo fails
        atexit.register(self.init_exit_handler)
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.create_clowder_repo(url, branch)
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
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        return repo.is_dirty()

    def link(self, version=None):
        """Create symlink pointing to clowder.yaml file"""
        if version is None:
            yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            path_output = fmt.path('.clowder/clowder.yaml')
        else:
            relative_path = os.path.join('.clowder', 'versions', version, 'clowder.yaml')
            path_output = fmt.path(relative_path)
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
        symlink_output = fmt.path('clowder.yaml')
        clowder_path = fmt.remove_prefix(real_path + '/', self.root_directory)
        path_output = fmt.path(clowder_path[1:-1])
        print(project_output + ' ' + current_ref_output)
        print(symlink_output + ' -> ' + path_output)
        print()

    def pull(self):
        """Pull clowder repo upstream changes"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.pull()

    def push(self):
        """Push clowder repo changes"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.push()

    def run_command(self, command):
        """Run command in clowder repo"""
        print(fmt.command(command))
        return_code = execute_subprocess_command(command.split(), self.clowder_path)
        if return_code != 0:
            print(fmt.command_failed_error(command))
            sys.exit(return_code)

    def git_status(self):
        """Print clowder repo git status"""
        repo = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        repo.status_verbose()

    def _validate_groups(self):
        """Validate status of clowder repo"""
        clowder = ProjectRepo(self.clowder_path, self.remote, self.default_ref)
        if not clowder.validate_repo():
            ProjectRepo.validation(self.clowder_path)
            print()
            sys.exit(1)


def subprocess_exit_handler(process):
    """terminate subprocess"""
    try:
        process.terminate()
    except:
        pass


def execute_subprocess_command(command, path, shell=True, env=None, stdout=None, stderr=None):
    """Run subprocess command"""
    try:
        process = subprocess.Popen(' '.join(command), shell=shell, env=env, cwd=path,
                                   stdout=stdout, stderr=stderr)
        atexit.register(subprocess_exit_handler, process)
        process.communicate()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        raise
    else:
        return process.returncode


def force_symlink(file1, file2):
    """Force symlink creation"""
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
