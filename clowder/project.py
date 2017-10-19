"""Representation of clowder.yaml project"""

from __future__ import print_function

import os
import sys

from clowder.utility.git.git_submodules import GitSubmodules
from termcolor import cprint
from clowder.utility.exception.clowder_exception import ClowderException
from clowder.fork import Fork
from clowder.utility.clowder_utilities import (
    execute_forall_command,
    existing_git_repository,
    is_offline
)
from clowder.utility.git.printing import (
    format_project_string,
    format_project_ref_string,
    print_exists,
    print_git_status,
    print_validation
)
from clowder.utility.git.git_repo import GitRepo
from clowder.utility.printing import (
    format_command,
    format_fork_string,
    format_remote_name_error,
    format_command_failed_error,
    print_invalid_yaml_error
)


class Project(object):
    """clowder.yaml project class"""

    def __init__(self, root_directory, project, group, defaults, sources):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']

        self.depth = project.get('depth', group.get('depth', defaults['depth']))
        self.recursive = project.get('recursive', group.get('recursive', defaults.get('recursive', False)))
        self.ref = project.get('ref', group.get('ref', defaults['ref']))
        self.remote_name = project.get('remote', group.get('remote', defaults['remote']))
        source_name = project.get('source', group.get('source', defaults['source']))

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.url = self.source.get_url_prefix() + self.name + ".git"

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            if fork['remote'] == self.remote_name:
                error = format_remote_name_error(fork['name'], self.name, self.remote_name)
                print_invalid_yaml_error()
                print(error + '\n')
                sys.exit(1)
            self.fork = Fork(fork, self.root_directory, self.path, self.source)

    def branch(self, local=False, remote=False):
        """Print branches for project"""
        self.print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        repo = GitRepo(self.full_path())
        if not is_offline():
            if remote:
                if self.fork is None:
                    repo.fetch(self.remote_name, depth=self.depth)
                else:
                    repo.fetch(self.fork.remote_name)
                    repo.fetch(self.remote_name)
        repo.print_branches(local=local, remote=remote)

    def clean(self, args='', recursive=False):
        """Discard changes for project"""
        self.print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        if self.recursive and recursive:
            repo = GitSubmodules(self.full_path())
            repo.clean(args=args)
        else:
            repo = GitRepo(self.full_path())
            repo.clean(args=args)

    def clean_all(self):
        """Discard all changes for project"""
        self.print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        if self.recursive:
            repo = GitSubmodules(self.full_path())
            repo.clean(args='fdx')
        else:
            repo = GitRepo(self.full_path())
            repo.clean(args='fdx')

    def diff(self):
        """Show git diff for project"""
        self.print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        print_git_status(self.full_path())

    def exists(self):
        """Check if project exists on disk"""
        path = os.path.join(self.full_path())
        return os.path.isdir(path)

    def existing_branch(self, branch, is_remote):
        """Check if branch exists"""
        repo = GitRepo(self.full_path())
        if is_remote:
            if self.fork is None:
                return repo.existing_remote_branch(branch, self.remote_name)
            return repo.existing_remote_branch(branch, self.fork.remote_name)
        return repo.existing_local_branch(branch)

    def fetch_all(self):
        """Fetch upstream changes if project exists on disk"""
        self.print_status()
        repo = GitRepo(self.full_path())
        if self.exists():
            if self.fork is None:
                repo.fetch(self.remote_name, depth=self.depth)
            else:
                repo.fetch(self.fork.remote_name)
                repo.fetch(self.remote_name)
        else:
            self.print_exists()

    def formatted_project_path(self):
        """Return formatted project path"""
        repo_path = os.path.join(self.root_directory, self.path)
        return format_project_string(repo_path, self.path)

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self, resolved=False):
        """Return python object representation for saving yaml"""
        if resolved:
            ref = self.ref
        else:
            repo = GitRepo(self.full_path())
            ref = repo.sha()
        project = {'name': self.name,
                   'path': self.path,
                   'depth': self.depth,
                   'recursive': self.recursive,
                   'ref': ref,
                   'remote': self.remote_name,
                   'source': self.source.name}
        if self.fork:
            fork_yaml = self.fork.get_yaml()
            project['fork'] = fork_yaml
        return project

    def herd(self, branch=None, tag=None, depth=None, rebase=False, print_output=True):
        """Clone project or update latest from upstream"""

        if depth is None:
            herd_depth = self.depth
        else:
            herd_depth = depth

        if branch:
            if self.recursive:
                repo = GitSubmodules(self.full_path(), print_output=print_output)
                self._herd_branch(repo, branch, herd_depth, rebase, print_output)
            else:
                repo = GitRepo(self.full_path(), print_output=print_output)
                self._herd_branch(repo, branch, herd_depth, rebase, print_output)
        elif tag:
            if self.recursive:
                repo = GitSubmodules(self.full_path(), print_output=print_output)
                self._herd_tag(repo, tag, herd_depth, rebase, print_output)
            else:
                repo = GitRepo(self.full_path(), print_output=print_output)
                self._herd_tag(repo, tag, herd_depth, rebase, print_output)
        else:
            if self.recursive:
                repo = GitSubmodules(self.full_path(), print_output=print_output)
                self._herd_ref(repo, herd_depth, rebase, print_output)
            else:
                repo = GitRepo(self.full_path(), print_output=print_output)
                self._herd_ref(repo, herd_depth, rebase, print_output)

    def is_dirty(self):
        """Check if project is dirty"""
        repo = GitRepo(self.full_path())
        if not repo.validate_repo():
            return True
        if self.recursive:
            repo_submodules = GitSubmodules(self.full_path())
            if repo_submodules.has_submodules():
                return True
        return False

    def is_valid(self):
        """Validate status of project"""
        repo = GitRepo(self.full_path())
        return repo.validate_repo()

    def print_exists(self):
        """Print existence validation message for project"""
        if not self.exists():
            self.print_status()
            print_exists(self.full_path())

    def print_status(self):
        """Print formatted project status"""
        if not existing_git_repository(self.full_path()):
            cprint(self.path, 'green')
            return
        project_output = format_project_string(self.full_path(), self.path)
        current_ref_output = format_project_ref_string(self.full_path())
        print(project_output + ' ' + current_ref_output)

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            self.print_status()
            print_validation(self.full_path())

    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branch"""
        if not existing_git_repository(self.full_path()):
            return
        if local and remote:
            self._prune_local(branch, force)
            self._prune_remote(branch)
        elif local:
            self._prune_local(branch, force)
        elif remote:
            self._prune_remote(branch)

    def reset(self, print_output=True):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD"""

        if self.recursive:
            repo = GitSubmodules(self.full_path(), print_output=print_output)
            self._reset(repo, print_output=print_output)
        else:
            repo = GitRepo(self.full_path(), print_output=print_output)
            self._reset(repo, print_output=print_output)

    def run(self, command, ignore_errors, print_output=True):
        """Run command or script in project directory"""

        if print_output:
            self.print_status()
            if not os.path.isdir(self.full_path()):
                cprint(" - Project is missing\n", 'red')
                return
            print(format_command(command))

        forall_env = {'CLOWDER_PATH': self.root_directory,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self.remote_name,
                      'PROJECT_REF': self.ref}
        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote_name

        return_code = execute_forall_command(command.split(),
                                             self.full_path(),
                                             forall_env,
                                             print_output)
        if not ignore_errors:
            err = format_command_failed_error(command)
            if return_code != 0:
                if print_output:
                    print(err)
                    sys.exit(return_code)
                raise ClowderException(err)

    def start(self, branch, tracking):
        """Start a new feature branch"""
        self.print_status()
        repo = GitRepo(self.full_path())
        if not existing_git_repository(self.full_path()):
            cprint(" - Directory doesn't exist", 'red')
            return
        if self.fork is None:
            remote = self.remote_name
            depth = self.depth
        else:
            remote = self.fork.remote_name
            depth = 0
        repo.start(remote, branch, depth, tracking)

    def status(self, padding):
        """Print status for project"""
        self._print_status_indented(padding)

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            self.print_status()
            repo = GitRepo(self.full_path())
            repo.stash()

    def sync(self, rebase=False, print_output=True):
        """Sync fork project with upstream"""
        if self.recursive:
            repo = GitSubmodules(self.full_path(), print_output=print_output)
            self._sync(repo, rebase, print_output)
        else:
            repo = GitRepo(self.full_path(), print_output=print_output)
            self._sync(repo, rebase, print_output)

    def _herd_branch(self, repo, branch, depth, rebase, print_output):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                self.print_status()
            repo.herd_branch(self.url, self.remote_name, branch, self.ref,
                             depth=depth, rebase=rebase)
        else:
            if print_output:
                self.fork.print_status()
            repo.configure_remotes(self.remote_name, self.url, self.fork.remote_name, self.fork.url)
            if print_output:
                print(format_fork_string(self.name))
            repo.herd_branch(self.url, self.remote_name, branch, self.ref, rebase=rebase,
                             fork_remote=self.fork.remote_name)
            if print_output:
                print(format_fork_string(self.fork.name))
            repo.herd_remote(self.fork.url, self.fork.remote_name, self.ref, branch=branch)

    def _herd_ref(self, repo, depth, rebase, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                self.print_status()
            repo.herd(self.url, self.remote_name, self.ref, depth=depth, rebase=rebase)
        else:
            if print_output:
                self.fork.print_status()
            repo.configure_remotes(self.remote_name, self.url, self.fork.remote_name, self.fork.url)
            if print_output:
                print(format_fork_string(self.name))
            repo.herd(self.url, self.remote_name, self.ref, rebase=rebase)
            if print_output:
                print(format_fork_string(self.fork.name))
            repo.herd_remote(self.fork.url, self.fork.remote_name, self.ref)

    def _herd_tag(self, repo, tag, depth, rebase, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                self.print_status()
            repo.herd_tag(self.url, self.remote_name, tag, self.ref,
                          depth=depth, rebase=rebase)
        else:
            if print_output:
                self.fork.print_status()
            repo.configure_remotes(self.remote_name, self.url,
                                   self.fork.remote_name, self.fork.url)
            if print_output:
                print(format_fork_string(self.name))
            repo.herd_tag(self.url, self.remote_name, tag, self.ref, rebase=rebase)
            if print_output:
                print(format_fork_string(self.fork.name))
            repo.herd_remote(self.fork.url, self.fork.remote_name, self.ref)

    def _print_status_indented(self, padding):
        """Print formatted and indented project status"""
        repo_path = os.path.join(self.root_directory, self.path)
        if not existing_git_repository(self.full_path()):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(repo_path, self.path)
        current_ref_output = format_project_ref_string(repo_path)
        print('{0} {1}'.format(project_output.ljust(padding), current_ref_output))

    def _prune_local(self, branch, force):
        """Prune local branch"""
        repo = GitRepo(self.full_path())
        if repo.existing_local_branch(branch):
            self.print_status()
            repo.prune_branch_local(branch, self.ref, force)

    def _prune_remote(self, branch):
        """Prune remote branch"""
        if self.fork is None:
            remote = self.remote_name
        else:
            remote = self.fork.remote_name
        repo = GitRepo(self.full_path())
        if repo.existing_remote_branch(branch, remote):
            self.print_status()
            repo.prune_branch_remote(branch, remote)

    def _reset(self, repo, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                self.print_status()
            repo.reset(self.remote_name, self.ref, depth=self.depth)
        else:
            if print_output:
                self.fork.print_status()
            repo.configure_remotes(self.remote_name, self.url, self.fork.remote_name, self.fork.url)
            if print_output:
                print(format_fork_string(self.name))
            repo.reset(self.remote_name, self.ref)

    def _sync(self, repo, rebase, print_output):
        """Sync fork project with upstream"""
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self.remote_name, self.url,
                               self.fork.remote_name, self.fork.url)
        if print_output:
            print(format_fork_string(self.name))
        repo.herd(self.url, self.remote_name, self.ref, rebase=rebase)
        if print_output:
            print(format_fork_string(self.fork.name))
        repo.herd_remote(self.fork.url, self.fork.remote_name, self.ref)
        if print_output:
            self.fork.print_status()
        repo.sync(self.remote_name, self.fork.remote_name, self.ref, rebase=rebase)
