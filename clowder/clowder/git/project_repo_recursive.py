# -*- coding: utf-8 -*-
"""Project Git utility class with submodules

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from git import GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.git.project_repo import ProjectRepo
from clowder.git.repo import execute_command


class ProjectRepoRecursive(ProjectRepo):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, remote, default_ref, parallel=False, print_output=True):
        ProjectRepo.__init__(self, repo_path, remote, default_ref, parallel=parallel, print_output=print_output)

    def clean(self, args=None):
        """Discard changes for repo and submodules"""

        ProjectRepo.clean(self, args=args)

        self._print(' - Clean submodules recursively')
        self._submodules_clean()

        self._print(' - Reset submodules recursively')
        self._submodules_reset()

        self._print(' - Update submodules recursively')
        self._submodules_update()

    def has_submodules(self):
        """Repo has submodules"""

        return len(self.repo.submodules) > 0

    def herd(self, url, depth=0, fetch=True, rebase=False):
        """Herd ref"""

        ProjectRepo.herd(self, url, depth=depth, fetch=fetch, rebase=rebase)
        self.submodule_update_recursive(depth)

    def herd_branch(self, url, branch, depth=0, rebase=False, fork_remote=None):
        """Herd branch"""

        ProjectRepo.herd_branch(self, url, branch, depth=depth, rebase=rebase, fork_remote=fork_remote)
        self.submodule_update_recursive(depth)

    def herd_tag(self, url, tag, depth=0, rebase=False):
        """Herd tag"""

        ProjectRepo.herd_tag(self, url, tag, depth=depth, rebase=rebase)
        self.submodule_update_recursive(depth)

    def is_dirty_submodule(self, path):
        """Check whether submodule repo is dirty"""

        return not self.repo.is_dirty(path)

    def submodule_update_recursive(self, depth=0):
        """Update submodules recursively and initialize if not present"""

        print(' - Recursively update and init submodules')

        if depth == 0:
            command = ['git', 'submodule', 'update', '--init', '--recursive']
        else:
            command = ['git', 'submodule', 'update', '--init', '--recursive', '--depth', depth]

        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to update submodules\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote"""

        ProjectRepo.sync(self, fork_remote, rebase=rebase)
        self.submodule_update_recursive()

    def validate_repo(self):
        """Validate repo state"""

        if not ProjectRepo.validate_repo(self):
            return False

        return not any([self.is_dirty_submodule(s.path) for s in self.repo.submodules])

    def _submodules_clean(self):
        """Clean all submodules"""

        self._submodule_command('foreach', '--recursive', 'git', 'clean', '-ffdx',
                                error_msg=' - Failed to clean submodules')

    def _submodule_command(self, *args, **kwargs):
        """Base submodule command"""

        try:
            self.repo.git.submodule(*args)
        except (GitError, ValueError) as err:
            message = colored(str(kwargs.get('error_msg', ' - Submodule command failed')), 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _submodules_reset(self):
        """Reset all submodules"""

        self._submodule_command('foreach', '--recursive', 'git', 'reset', '--hard',
                                error_msg=' - Failed to reset submodules')

    def _submodules_update(self):
        """Update all submodules"""

        self._submodule_command('update', '--checkout', '--recursive', '--force',
                                error_msg=' - Failed to update submodules')
