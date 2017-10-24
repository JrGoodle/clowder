"""Representation of clowder.yaml project"""

from __future__ import print_function

import os
import sys

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.git.project_repo import ProjectRepo
from clowder.git.project_repo_recursive import ProjectRepoRecursive
from clowder.model.fork import Fork
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_forall_command


class Project(object):
    """clowder.yaml project class"""

    def __init__(self, root_directory, project, group, defaults, sources):
        self.name = project['name']
        self.path = project['path']

        self._root_directory = root_directory
        self._ref = project.get('ref', group.get('ref', defaults['ref']))
        self._remote = project.get('remote', group.get('remote', defaults['remote']))
        self._depth = project.get('depth', group.get('depth', defaults['depth']))
        self._recursive = project.get('recursive', group.get('recursive', defaults.get('recursive', False)))
        self._timestamp_author = project.get('timestamp_author', group.get('timestamp_author',
                                                                           defaults.get('timestamp_author', None)))

        self._source = None
        source_name = project.get('source', group.get('source', defaults['source']))
        for source in sources:
            if source.name == source_name:
                self._source = source

        self._url = self._source.get_url_prefix() + self.name + ".git"

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            if fork['remote'] == self._remote:
                error = fmt.remote_name_error(fork['name'], self.name, self._remote)
                print(fmt.invalid_yaml_error())
                print(error + '\n')
                sys.exit(1)
            self.fork = Fork(fork, self._root_directory, self.path, self._source)

    def branch(self, local=False, remote=False):
        """Print branches for project"""
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not is_offline():
            if remote:
                if self.fork is None:
                    repo.fetch(self._remote, depth=self._depth)
                else:
                    repo.fetch(self.fork.remote_name)
                    repo.fetch(self._remote)
        repo.print_branches(local=local, remote=remote)

    def clean(self, args='', recursive=False):
        """Discard changes for project"""
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive and recursive)
        repo.clean(args=args)

    def clean_all(self):
        """Discard all changes for project"""
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive)
        repo.clean(args='fdx')

    def diff(self):
        """Show git diff for project"""
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
            return
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        repo.status_verbose()

    def exists(self):
        """Check if project exists on disk"""
        path = os.path.join(self.full_path())
        return os.path.isdir(path)

    def existing_branch(self, branch, is_remote):
        """Check if branch exists"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if is_remote:
            if self.fork is None:
                return repo.existing_remote_branch(branch, self._remote)
            return repo.existing_remote_branch(branch, self.fork.remote_name)
        return repo.existing_local_branch(branch)

    def fetch_all(self):
        """Fetch upstream changes if project exists on disk"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if self.exists():
            if self.fork is None:
                repo.fetch(self._remote, depth=self._depth)
            else:
                repo.fetch(self.fork.remote_name)
                repo.fetch(self._remote)
        else:
            self.print_exists()

    def formatted_project_path(self):
        """Return formatted project path"""
        repo_path = os.path.join(self._root_directory, self.path)
        return ProjectRepo.format_project_string(repo_path, self.path)

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self._root_directory, self.path)

    def get_current_timestamp(self):
        """Clone project or update latest from upstream"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        return repo.get_current_timestamp()

    def get_yaml(self, resolved=False):
        """Return python object representation for saving yaml"""
        if resolved:
            ref = self._ref
        else:
            repo = ProjectRepo(self.full_path(), self._remote, self._ref)
            ref = repo.sha()
        project = {'name': self.name,
                   'path': self.path,
                   'depth': self._depth,
                   'recursive': self._recursive,
                   'ref': ref,
                   'remote': self._remote,
                   'source': self._source.name}
        if self.fork:
            fork_yaml = self.fork.get_yaml()
            project['fork'] = fork_yaml
        if self._timestamp_author:
            project['timestamp_author'] = self._timestamp_author
        return project

    def herd(self, branch=None, tag=None, depth=None, rebase=False, parallel=False):
        """Clone project or update latest from upstream"""

        print_output = not parallel

        if depth is None:
            herd_depth = self._depth
        else:
            herd_depth = depth

        if branch:
            repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                              parallel=parallel, print_output=print_output)
            self._herd_branch(repo, branch, herd_depth, rebase, print_output)
        elif tag:
            repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                              parallel=parallel, print_output=print_output)
            self._herd_tag(repo, tag, herd_depth, rebase, print_output)
        else:
            repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                              parallel=parallel, print_output=print_output)
            self._herd_ref(repo, herd_depth, rebase, print_output)

    def is_dirty(self):
        """Check if project is dirty"""
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive)
        return not repo.validate_repo()

    def is_valid(self):
        """Validate status of project"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        return repo.validate_repo()

    def print_exists(self):
        """Print existence validation message for project"""
        if not self.exists():
            print(self.status())
            ProjectRepo.exists(self.full_path())

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            print(self.status())
            ProjectRepo.validation(self.full_path())

    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branch"""
        if not ProjectRepo.existing_git_repository(self.full_path()):
            return
        if local and remote:
            self._prune_local(branch, force)
            self._prune_remote(branch)
        elif local:
            self._prune_local(branch, force)
        elif remote:
            self._prune_remote(branch)

    def reset(self, timestamp=None, parallel=False):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD"""

        print_output = not parallel
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                          parallel=parallel, print_output=print_output)
        self._reset(repo, timestamp=timestamp, print_output=print_output)

    def run(self, command, ignore_errors, parallel=False):
        """Run command or script in project directory"""

        print_output = not parallel

        if print_output:
            if not os.path.isdir(self.full_path()):
                cprint(" - Project is missing\n", 'red')
                return
            print(fmt.command(command))

        forall_env = {'CLOWDER_PATH': self._root_directory,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self._remote,
                      'PROJECT_REF': self._ref}
        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote_name

        return_code = execute_forall_command(command.split(),
                                             self.full_path(),
                                             forall_env,
                                             print_output)
        if not ignore_errors:
            err = fmt.command_failed_error(command)
            if return_code != 0:
                if print_output:
                    print(err)
                    sys.exit(return_code)
                raise ClowderError(err)

    def start(self, branch, tracking):
        """Start a new feature branch"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not ProjectRepo.existing_git_repository(self.full_path()):
            cprint(" - Directory doesn't exist", 'red')
            return
        if self.fork is None:
            remote = self._remote
            depth = self._depth
        else:
            remote = self.fork.remote_name
            depth = 0
        repo.start(remote, branch, depth, tracking)

    def status(self, padding=None):
        """Return formatted status for project"""
        if not ProjectRepo.existing_git_repository(self.full_path()):
            cprint(self.name, 'green')
            return
        project_output = ProjectRepo.format_project_string(self.full_path(), self.path)
        current_ref_output = ProjectRepo.format_project_ref_string(self.full_path())
        if padding:
            project_output = project_output.ljust(padding)
        return project_output + ' ' + current_ref_output

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            repo = ProjectRepo(self.full_path(), self._remote, self._ref)
            repo.stash()

    def sync(self, rebase=False, parallel=False):
        """Sync fork project with upstream"""

        print_output = not parallel
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                          parallel=parallel, print_output=print_output)
        self._sync(repo, rebase, print_output)

    def _herd_branch(self, repo, branch, depth, rebase, print_output):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                print(self.status())
            repo.herd_branch(self._url, branch, depth=depth, rebase=rebase)
            return
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)
        if print_output:
            print(fmt.fork_string(self.name))
        repo.herd_branch(self._url, branch, rebase=rebase, fork_remote=self.fork.remote_name)
        if print_output:
            print(fmt.fork_string(self.fork.name))
        repo.herd_remote(self.fork.url, self.fork.remote_name, branch=branch)

    def _herd_ref(self, repo, depth, rebase, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                print(self.status())
            repo.herd(self._url, depth=depth, rebase=rebase)
            return
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)
        if print_output:
            print(fmt.fork_string(self.name))
        repo.herd(self._url, rebase=rebase)
        if print_output:
            print(fmt.fork_string(self.fork.name))
        repo.herd_remote(self.fork.url, self.fork.remote_name)

    def _herd_tag(self, repo, tag, depth, rebase, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                print(self.status())
            repo.herd_tag(self._url, tag, depth=depth, rebase=rebase)
            return
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)
        if print_output:
            print(fmt.fork_string(self.name))
        repo.herd_tag(self._url, tag, rebase=rebase)
        if print_output:
            print(fmt.fork_string(self.fork.name))
        repo.herd_remote(self.fork.url, self.fork.remote_name)

    def _prune_local(self, branch, force):
        """Prune local branch"""
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if repo.existing_local_branch(branch):
            repo.prune_branch_local(branch, force)

    def _prune_remote(self, branch):
        """Prune remote branch"""
        if self.fork is None:
            remote = self._remote
        else:
            remote = self.fork.remote_name
        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if repo.existing_remote_branch(branch, remote):
            repo.prune_branch_remote(branch, remote)

    @staticmethod
    def _repo(path, remote, ref, recursive, **kwargs):
        """Clone project or update latest from upstream"""
        if recursive:
            return ProjectRepoRecursive(path, remote, ref, **kwargs)
        return ProjectRepo(path, remote, ref, **kwargs)

    def _reset(self, repo, timestamp=None, print_output=True):
        """Clone project or update latest from upstream"""
        if self.fork is None:
            if print_output:
                print(self.status())
            if timestamp:
                repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
                return
            repo.reset(depth=self._depth)
            return
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)
        if print_output:
            print(fmt.fork_string(self.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
            return
        repo.reset()

    def _sync(self, repo, rebase, print_output):
        """Sync fork project with upstream"""
        if print_output:
            self.fork.print_status()
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)
        if print_output:
            print(fmt.fork_string(self.name))
        repo.herd(self._url, self._remote, rebase=rebase)
        if print_output:
            print(fmt.fork_string(self.fork.name))
        repo.herd_remote(self.fork.url, self.fork.remote_name)
        if print_output:
            self.fork.print_status()
        repo.sync(self.fork.remote_name, rebase=rebase)
