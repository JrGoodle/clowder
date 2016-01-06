"""Representation of clowder.yaml project"""
import os, subprocess
from termcolor import colored, cprint
from clowder.fork import Fork
from clowder.utility.clowder_utilities import (
    format_project_string,
    format_ref_string,
    print_exists,
    print_validation,
    validate_repo_state
)
from clowder.utility.git_utilities import (
    git_checkout_ref,
    git_create_repo,
    git_create_remote,
    git_current_sha,
    git_fetch_remote_ref,
    git_is_dirty,
    git_pull_remote_branch,
    git_ref_type,
    git_reset_head,
    git_stash,
    git_status,
    git_truncate_ref
)


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
                self.forks.append(Fork(fork['name'], full_path, self.source,
                                       fork['remote'], self.depth))

    def exists(self):
        """Check if project exists on disk"""
        path = os.path.join(self.full_path(), '.git')
        return os.path.isdir(path)

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        forks_yaml = [f.get_yaml() for f in self.forks]
        return {'name': self.name,
                'path': self.path,
                'depth': self.depth,
                'forks': forks_yaml,
                'ref': git_current_sha(self.full_path()),
                'remote': self.remote_name,
                'source': self.source.name}

    def clean(self):
        """Discard changes for project"""
        if self.is_dirty():
            self._print_status()
            print(' - Discarding current changes')
            git_reset_head(self.full_path())

    def herd(self):
        """Clone project or update latest from upstream"""
        self._print_status()
        if not os.path.isdir(os.path.join(self.full_path(), '.git')):
            git_create_repo(self.url, self.full_path(), self.remote_name,
                            self.ref, self.depth)
        else:
            ref_type = git_ref_type(self.ref)
            if ref_type is 'branch':
                git_create_remote(self.full_path(), self.remote_name, self.url)
                git_fetch_remote_ref(self.full_path(), self.remote_name,
                                     self.ref, self.depth)
                git_checkout_ref(self.full_path(), self.ref, self.remote_name)
                branch = git_truncate_ref(self.ref)
                git_pull_remote_branch(self.full_path(), self.remote_name, branch)
            elif ref_type is 'tag' or ref_type is 'sha':
                git_create_remote(self.full_path(), self.remote_name, self.url)
                git_fetch_remote_ref(self.full_path(), self.remote_name,
                                     self.ref, self.depth)
                git_checkout_ref(self.full_path(), self.ref, self.remote_name)
            else:
                cprint('Unknown ref ' + self.ref, 'red')

        for fork in self.forks:
            fork.herd()

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path())

    def is_valid(self):
        """Validate status of project"""
        return validate_repo_state(self.full_path())

    def status(self):
        """Print status for project"""
        self._print_status()

    def status_verbose(self):
        """Print verbose status for project"""
        self._print_status()
        git_status(self.full_path())

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            self._print_status()
            git_stash(self.full_path())

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

    def _print_status(self):
        """Print formatted project status"""
        repo_path = os.path.join(self.root_directory, self.path)
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(repo_path, self.name)
        current_ref_output = format_ref_string(repo_path)
        print(project_output + ' ' + current_ref_output)
        cprint(self.path, 'cyan')

    def run_command(self, command):
        """Run command in project directory"""
        self._print_status()
        command_output = colored('$ ' + command, attrs=['bold'])
        print(command_output)
        subprocess.call(command.split(), cwd=self.full_path())
        print('')
