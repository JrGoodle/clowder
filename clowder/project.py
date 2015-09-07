"""Representation of clowder.yaml project"""
import os
from termcolor import colored, cprint
from clowder.utility.clowder_utilities import (
    format_project_string,
    format_ref_string,
    groom,
    herd,
    print_exists,
    print_validation,
    validate_repo_state
)
from clowder.utility.git_utilities import (
    git_current_sha,
    git_is_dirty,
    git_stash,
    git_status
)


class Project(object):
    """clowder.yaml project class"""

    def __init__(self, root_directory, project, defaults, sources):
        self.root_directory = root_directory
        self.name = project['name']
        self.path = project['path']

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

    def full_path(self):
        """Return full path to project"""
        return os.path.join(self.root_directory, self.path)

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name,
                'path': self.path,
                'ref': git_current_sha(self.full_path()),
                'remote': self.remote_name,
                'source': self.source.name}

    def groom(self):
        """Discard changes for project"""
        if self.is_dirty():
            self._print_status()
            groom(self.full_path())

    def herd(self):
        """Clone project or update latest from upstream"""
        self._print_status()
        herd(self.full_path(), self.ref, self.remote_name, self.url)

    def is_dirty(self):
        """Check if project is dirty"""
        return git_is_dirty(self.full_path())

    def exists(self):
        """Check if project exists on disk"""
        path = os.path.join(self.full_path(), '.git')
        return os.path.isdir(path)

    def meow(self):
        """Print status for project"""
        self._print_status()

    def meow_verbose(self):
        """Print verbose status for project"""
        self._print_status()
        git_status(self.full_path())

    def stash(self):
        """Stash changes for project if dirty"""
        if self.is_dirty():
            self._print_status()
            git_stash(self.full_path())

    def is_valid(self):
        """Validate status of project"""
        return validate_repo_state(self.full_path())

    def _print_status(self):
        """Print formatted project status"""
        repo_path = os.path.join(self.root_directory, self.path)
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            cprint(self.name, 'green')
            return
        project_output = format_project_string(repo_path, self.name)
        current_ref_output = format_ref_string(repo_path)
        path_output = colored(self.path, 'cyan')
        print(project_output + ' ' + current_ref_output + ' ' + path_output)

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
