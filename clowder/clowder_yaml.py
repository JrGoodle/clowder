"""clowder.yaml parsing and functionality"""
import os, subprocess, sys, yaml
from termcolor import colored
from clowder.group import Group
from clowder.source import Source
from clowder.utility.clowder_utilities import (
    print_clowder_repo_status,
    print_exiting
)

class ClowderYAML(object):
    """Class encapsulating project information from clowder.yaml"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.default_ref = None
        self.default_remote = None
        self.default_source = None
        self.groups = []
        self.sources = []

        self._load_yaml()

        self.group_names = [g.name for g in self.groups]
        self.group_names.sort()

    def fix_version(self, version):
        """Fix current commits to versioned clowder.yaml"""
        self._validate(self.group_names)
        versions_dir = os.path.join(self.root_directory, 'clowder', 'versions')
        version_dir = os.path.join(versions_dir, version)
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        yaml_file_output = colored(yaml_file, 'cyan')
        version_output = colored(version, attrs=['bold'])
        if not os.path.exists(yaml_file):
            with open(yaml_file, 'w') as file:
                print('Fixing version ' + version_output + ' at ' + yaml_file_output)
                yaml.dump(self._get_yaml(), file, default_flow_style=False)
        else:
            print('Version ' + version_output + ' already exists at ' + yaml_file_output)
            print_exiting()

    def forall(self, command, group_names):
        """Runs command in all projects of groups specified"""
        directories = []
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    directories.append(project.full_path())
        _forall_run(command, directories)

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        names = [g.get_all_project_names() for g in self.groups]
        return names.sort()

    def get_fixed_version_names(self):
        """Return list of all fixed versions"""
        versions_dir = os.path.join(self.root_directory, 'clowder', 'versions')
        if os.path.exists(versions_dir):
            return os.listdir(versions_dir)
        else:
            return None

    def groom(self, group_names):
        """Discard changes for all projects"""
        print_clowder_repo_status(self.root_directory)
        print('')
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.groom()
        else:
            print('No changes to discard')

    def herd(self, group_names):
        """Sync all projects with latest upstream changes"""
        self._validate(group_names)
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            if group.name in group_names:
                group.herd()

    def meow(self, group_names):
        """Print status for all projects"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            if group.name in group_names:
                group.meow()

    def meow_verbose(self, group_names):
        """Print git status for all projects with changes"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            if group.name in group_names:
                group.meow_verbose()

    def stash(self, group_names):
        """Stash changes for all projects with changes"""
        print_clowder_repo_status(self.root_directory)
        print('')
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.stash()
        else:
            print('No changes to stash')

    def _get_yaml(self):
        """Return python object representation for saving yaml"""
        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        defaults_yaml = {'ref': self.default_ref,
                         'remote': self.default_remote,
                         'source': self.default_source}
        return {'defaults': defaults_yaml,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def _is_dirty(self):
        """Check if there are any dirty projects"""
        is_dirty = False
        for group in self.groups:
            if group.is_dirty():
                is_dirty = True
        return is_dirty

    def _load_yaml(self):
        """Load clowder from yaml file"""
        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.exists(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)
                _validate_yaml(parsed_yaml)

                self.default_ref = parsed_yaml['defaults']['ref']
                self.default_remote = parsed_yaml['defaults']['remote']
                self.default_source = parsed_yaml['defaults']['source']

                self.sources = [Source(s) for s in parsed_yaml['sources']]

                defaults = {'ref': self.default_ref,
                            'remote': self.default_remote,
                            'source': self.default_source}

                for group in parsed_yaml['groups']:
                    self.groups.append(Group(self.root_directory,
                                             group,
                                             defaults,
                                             self.sources))
                # self.groups.sort(key=lambda group: group.name)

    def _validate(self, group_names):
        """Validate status of all projects for specified groups"""
        valid = True
        for group in self.groups:
            if group.name in group_names:
                group.print_validation()
                if not group.is_valid():
                    valid = False
        if not valid:
            print_exiting()

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104
def _validate_yaml(parsed_yaml):
    """Load clowder from yaml file"""
    try:
        parsed_yaml['defaults']['ref']
        parsed_yaml['defaults']['remote']
        parsed_yaml['defaults']['source']

        for source in parsed_yaml['sources']:
            source['name']
            source['url']

        for group in parsed_yaml['groups']:
            group['name']
            for project in group['projects']:
                project['name']
                project['path']
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print_exiting()

def _forall_run(command, directories):
    """Run command in all directories"""
    sorted_paths = sorted(set(directories))
    paths = [p for p in sorted_paths if os.path.isdir(p)]
    for path in paths:
        running_output = colored('Running command', attrs=['underline'])
        command_output = colored(command, attrs=['bold'])
        print(running_output + ': ' + command_output)
        directory_output = colored('Directory', attrs=['underline'])
        path_output = colored(path, 'cyan')
        print(directory_output + ': ' + path_output)
        subprocess.call(command.split(),
                        cwd=path)
        print('')
    sys.exit()
