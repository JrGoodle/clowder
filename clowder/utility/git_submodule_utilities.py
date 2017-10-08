"""Git utilities"""


import sys
from termcolor import cprint
from clowder.utility.clowder_utilities import (
    execute_command,
    existing_git_repository
)
from clowder.utility.git_utilities import Git
from clowder.utility.print_utilities import (
    print_command_failed_error,
    print_error
)


# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703
# Disable errors shown by pylint for too many arguments
# pylint: disable=R0913


class GitSubmodules(Git):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path):
        Git.__init__(self, repo_path)

    def clean(self, args=None):
        """Discard changes for repo and submodules"""
        Git.clean(self, args=args)
        print(' - Clean submodules recursively')
        self._submodules_clean()
        print(' - Reset submodules recursively')
        self._submodules_reset()
        print(' - Update submodules recursively')
        self._submodules_update()

    def create_repo(self, url, remote, ref, depth=0):
        """Clone git repo from url at path"""
        Git.create_repo(self, url, remote, ref, depth=depth)
        self.submodule_update_recursive(depth)

    def has_submodules(self):
        """Repo has submodules"""
        return self.repo.submodules.count > 0

    def herd(self, url, remote, ref, depth=0, fetch=True, rebase=False):
        """Herd ref"""
        Git.herd(self, url, remote, ref, depth=depth, fetch=fetch, rebase=rebase)
        self.submodule_update_recursive(depth)

    def herd_branch(self, url, remote, branch, default_ref, depth=0, rebase=False):
        """Herd branch"""
        Git.herd_branch(self, url, remote, branch, default_ref, depth=depth, rebase=rebase)
        self.submodule_update_recursive(depth)

    def is_dirty_submodule(self, path):
        """Check whether submodule repo is dirty"""
        return not self.repo.is_dirty(path)

    def submodule_update_recursive(self, depth=0):
        """Update submodules recursively and initialize if not present"""
        print(' - Update submodules recursively and initialize if not present')
        if depth == 0:
            command = ['git', 'submodule', 'update', '--init', '--recursive']
        else:
            command = ['git', 'submodule', 'update', '--init', '--recursive', '--depth', depth]
        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            cprint(' - Failed to update submodules', 'red')
            print_command_failed_error(command)
            sys.exit(return_code)

    def sync(self, upstream_remote, fork_remote, ref):
        """Sync fork with upstream remote"""
        Git.sync(self, upstream_remote, fork_remote, ref)
        self.submodule_update_recursive()

    def validate_repo(self):
        """Validate repo state"""
        if not existing_git_repository(self.repo_path):
            return True
        if not self.is_dirty():
            return False
        for submodule in self.repo.submodules:
            if not self.is_dirty_submodule(submodule.path):
                return False
        return True

    def _create_repo_herd_branch(self, url, remote, branch, default_ref, depth=0):
        """Clone git repo from url at path for herd branch"""
        Git._create_repo_herd_branch(self, url, remote, branch, default_ref, depth=depth)
        self.submodule_update_recursive(depth=depth)

    def _submodules_clean(self):
        """Clean all submodules"""
        try:
            self.repo.git.submodule('foreach', '--recursive', 'git', 'clean', '-ffdx')
        except Exception as err:
            cprint(' - Failed to clean submodules', 'red')
            print_error(err)
            sys.exit(1)

    def _submodules_reset(self):
        """Reset all submodules"""
        try:
            self.repo.git.submodule('foreach', '--recursive', 'git', 'reset', '--hard')
        except Exception as err:
            cprint(' - Failed to reset submodules', 'red')
            print_error(err)
            sys.exit(1)

    def _submodules_update(self):
        """Update all submodules"""
        try:
            self.repo.git.submodule('update', '--checkout', '--recursive', '--force')
        except Exception as err:
            cprint(' - Failed to update submodules', 'red')
            print_error(err)
            sys.exit(1)
