"""Representation of clowder.yaml project"""
import os
import sys
from termcolor import cprint
from clowder.fork import Fork
from clowder.utility.clowder_utilities import execute_command
from clowder.utility.print_utilities import (
    format_command,
    format_path,
    print_command_failed_error
)
from clowder.utility.git_print_utilities import (
    format_project_string,
    format_project_ref_string,
    print_exists,
    print_validation
)
from clowder.utility.git_utilities import (
    git_create_repo,
    git_existing_local_branch,
    git_existing_remote_branch,
    git_existing_repository,
    git_fetch_all,
    git_fetch_silent,
    git_herd,
    git_is_dirty,
    git_prune_local,
    git_prune_remote,
    git_reset_head,
    git_sha_long,
    git_start,
    git_stash,
    git_status,
    git_validate_repo_state
)

# Disable errors shown by pylint for too many instance attributes
# pylint: disable=R0902
# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703

class Project(object):
    """clowder.yaml project class"""

    def __init__(self, root_directory, project, defaults, sources):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']

        if 'depth' in project:
            self.depth = project['depth']
        else:
            self.depth = defaults['depth']

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults['ref']

        if 'remote' in project:
            self.remote_name = project['remote']
        else:
            self.remote_name = defaults['remote']

        if 'source' in project:
            source_name = project['source']
        else:
            source_name = defaults['source']

        for source in sources:
            if source.name == source_name:
                self.source = source

        self.url = self.source.get_url_prefix() + self.name + ".git"

        self.forks = []
        if 'forks' in project:
            for fork in project['forks']:
                full_path = os.path.join(self.root_directory, self.path)
                self.forks.append(Fork(fork, full_path, self.source))

    def clean(self):
        """Discard changes for project"""
        if self.is_dirty():
            self._print_status()
            print(' - Discard current changes')
            git_reset_head(self.full_path())

    def diff(self):
        """Show git diff for project"""
        self._print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
        else:
            git_status(self.full_path())

    def exists(self):
        """Check if project exists on disk"""
        path = os.path.join(self.full_path())
        return os.path.isdir(path)

    def existing_local_branch(self, branch):
        """Check if local branch exists"""
        return git_existing_local_branch(self.full_path(), branch)

    def existing_remote_branch(self, branch):
        """Check if remote branch exists"""
        return git_existing_remote_branch(self.full_path(), branch, self.remote_name)

    def fetch_all(self):
        """Fetch upstream changes if project exists on disk"""
        self._print_status()
        if self.exists():
            git_fetch_all(self.full_path())
        else:
            self.print_exists()

    def fetch_silent(self):
        """Silently fetch upstream changes if project exists on disk"""
        if self.exists():
            git_fetch_silent(self.full_path())

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        project = {'name': self.name,
                   'path': self.path,
                   'depth': self.depth,
                   'ref': git_sha_long(self.full_path()),
                   'remote': self.remote_name,
                   'source': self.source.name}
        forks_yaml = [f.get_yaml() for f in self.forks]
        if len(forks_yaml) > 0:
            project['forks'] = forks_yaml
        return project

    def herd(self, branch=None, depth=None):
        """Clone project or update latest from upstream"""
        self._print_status()
        if branch is None:
            ref = self.ref
        else:
            ref = 'refs/heads/' + branch

        if depth is None:
            herd_depth = self.depth
        else:
            herd_depth = depth

        if not git_existing_repository(self.full_path()):
            git_create_repo(self.url, self.full_path(), self.remote_name,
                            ref, herd_depth)
        else:
            git_herd(self.full_path(), self.url, self.remote_name, ref, herd_depth)

        for fork in self.forks:
            fork.herd(ref, herd_depth)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path())

    def is_valid(self):
        """Validate status of project"""
        return git_validate_repo_state(self.full_path())

    def print_exists(self):
        """Print existence validation message for project"""
        if not self.exists():
            self._print_status()
            print_exists(self.full_path())

    def print_validation(self):
        """Print validation message for project"""
        if not self.is_valid():
            self._print_status()
            print_validation(self.full_path())

    def prune_all(self, branch, force):
        """Prune local and remote branches"""
        if git_existing_repository(self.full_path()):
            local_branch_exists = git_existing_local_branch(self.full_path(), branch)
            remote_branch_exists = git_existing_remote_branch(self.full_path(),
                                                              branch, self.remote_name)
            if local_branch_exists or remote_branch_exists:
                self._print_status()
                if local_branch_exists:
                    git_prune_local(self.full_path(), branch, self.ref, force)
                if remote_branch_exists:
                    git_prune_remote(self.full_path(), branch, self.remote_name)

    def prune_local(self, branch, force):
        """Prune local branch"""
        if git_existing_repository(self.full_path()):
            if git_existing_local_branch(self.full_path(), branch):
                self._print_status()
                git_prune_local(self.full_path(), branch, self.ref, force)

    def prune_remote(self, branch):
        """Prune remote branch"""
        if git_existing_repository(self.full_path()):
            if git_existing_remote_branch(self.full_path(), branch, self.remote_name):
                self._print_status()
                git_prune_remote(self.full_path(), branch, self.remote_name)

    def run(self, command, ignore_errors):
        """Run command or script in project directory"""
        self._print_status()
        if not os.path.isdir(self.full_path()):
            cprint(" - Project is missing\n", 'red')
        else:
            print(format_command(command))
            return_code = execute_command(command.split(), self.full_path())
            if not ignore_errors:
                if return_code != 0:
                    print_command_failed_error(command)
                    sys.exit(return_code)

    def start(self, branch, tracking):
        """Start a new feature branch"""
        self._print_status()
        if not git_existing_repository(self.full_path()):
            cprint(" - Directory doesn't exist", 'red')
        else:
            git_start(self.full_path(), self.remote_name, branch, self.depth, tracking)

    def status(self):
        """Print status for project"""
        self._print_status()

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            self._print_status()
            git_stash(self.full_path())

# Disable warning for unused variables
# pylint: disable=W0612
# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

    def _print_status(self):
        """Print formatted project status"""
        repo_path = os.path.join(self.root_directory, self.path)
        if not git_existing_repository(repo_path):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(repo_path, self.name)
        current_ref_output = format_project_ref_string(repo_path)
        path_output = format_path(self.path)
        long_output = project_output + ' ' + current_ref_output + ' -> ' + path_output
        short_output = project_output + ' ' + current_ref_output + '\n-> ' + path_output
        long_output_length = len(''.join(s for s in long_output if ord(s) > 31 and ord(s) < 126))
        try:
            terminal_size = os.get_terminal_size()
            if long_output_length <= terminal_size.columns:
                print(long_output)
            else:
                print(short_output)
        except:
            print(long_output)
