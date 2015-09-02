"""clowder.yaml parsing and functionality"""
import os, subprocess, sys, yaml
from termcolor import colored, cprint
from clowder.model.group import Group
from clowder.model.remote import Remote
from clowder.utility.git_utilities import (
    git_stash,
    git_validate_repo_state
)
from clowder.utility.print_utilities import (
    print_clowder_repo_status,
    print_group,
    print_project_status,
    print_running_command,
    print_verbose_status
)

class ClowderYAML(object):
    """Class encapsulating project information from clowder.yaml"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.default_ref = None
        self.default_remote = None
        self.groups = []
        self.remotes = []

        self._load_yaml()

        self.group_names = []
        for group in self.groups:
            self.group_names.append(group.name)
        self.group_names.sort()

    def fix_version(self, version):
        """Fix current commits to versioned clowder.yaml"""
        self._validate_all()
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
            print('')
            cprint('Exiting...', 'red')
            print('')
            sys.exit()

    def forall(self, command):
        """Runs command in all projects"""
        for group in self.groups:
            print_group(group.name)
            for project in group.projects:
                if os.path.isdir(project.full_path):
                    print_project_status(self.root_directory, project.path, project.name)
                    print_running_command(command)
                    subprocess.call(command.split(),
                                    cwd=project.full_path)

    def forall_groups(self, command, group_names):
        """Runs command in all projects"""
        for group in self.groups:
            if group.name in group_names:
                print_group(group.name)
                for project in group.projects:
                    if os.path.isdir(project.full_path):
                        print_project_status(self.root_directory, project.path, project.name)
                        print_running_command(command)
                        subprocess.call(command.split(),
                                        cwd=project.full_path)

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        names = []
        for group in self.groups:
            names.extend(group.get_all_project_names())
        return names.sort()

    def get_fixed_version_names(self):
        """Return list of all fixed versions"""
        versions_dir = os.path.join(self.root_directory, 'clowder', 'versions')
        if os.path.exists(versions_dir):
            return os.listdir(versions_dir)
        else:
            return None

    def groom(self):
        """Discard changes for all projects"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            group.groom()

    def herd_all(self):
        """Sync all projects with latest upstream changes"""
        self._validate_all()
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            print_group(group.name)
            for project in group.projects:
                print_project_status(self.root_directory, project.path, project.name)
                project.herd()

    def herd_groups(self, group_names):
        """Sync all projects with latest upstream changes"""
        self._validate_groups(group_names)
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            if group.name in group_names:
                print_group(group.name)
                for project in group.projects:
                    print_project_status(self.root_directory, project.path, project.name)
                    project.herd()

    def herd_version(self, version):
        """Sync all projects to fixed versions"""
        self._validate_all()
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            print_group(group.name)
            for project in group.projects:
                print_project_status(self.root_directory, project.path, project.name)
                project.herd_version(version)

    def meow(self):
        """Print status for all projects"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            print_group(group.name)
            for project in group.projects:
                print_project_status(self.root_directory, project.path, project.name)

    def meow_verbose(self):
        """Print git status for all projects with changes"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            print_group(group.name)
            for project in group.projects:
                print_project_status(self.root_directory, project.path, project.name)
                print_verbose_status(project.full_path)

    def stash(self):
        """Stash changes for all projects with changes"""
        print_clowder_repo_status(self.root_directory)
        print('')
        for group in self.groups:
            if group.is_dirty:
                print_group(group.name)
                for project in group.projects:
                    print_project_status(self.root_directory, project.path, project.name)
                    git_stash(project.full_path)

    def _get_yaml(self):
        """Return python object representation for saving yaml"""
        groups_yaml = []
        for group in self.groups:
            groups_yaml.append(group.get_yaml())

        remotes_yaml = []
        for remote in self.remotes:
            remotes_yaml.append(remote.get_yaml())

        defaults_yaml = {'ref': self.default_ref, 'remote': self.default_remote}

        return {'defaults': defaults_yaml,
                'remotes': remotes_yaml,
                'groups': groups_yaml}

    def _load_yaml(self):
        """Load clowder from yaml file"""
        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.exists(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)

                self.default_ref = parsed_yaml['defaults']['ref']
                self.default_remote = parsed_yaml['defaults']['remote']

                for remote in parsed_yaml['remotes']:
                    self.remotes.append(Remote(remote))

                defaults = {'ref': self.default_ref, 'remote': self.default_remote}

                for group in parsed_yaml['groups']:
                    self.groups.append(Group(self.root_directory,
                                             group,
                                             defaults,
                                             self.remotes))
                # self.groups.sort(key=lambda group: group.name)

    def _validate_all(self):
        """Validate status of all projects"""
        for group in self.groups:
            for project in group.projects:
                git_validate_repo_state(project.full_path)

    def _validate_groups(self, group_names):
        """Validate status of all projects"""
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    git_validate_repo_state(project.full_path)
