"""clowder.yaml parsing and functionality"""
import os
import yaml

from clowder.utility.git_utilities import git_status

from clowder.model.group import Group
from clowder.model.remote import Remote

class ClowderYAML(object):
    """Class encapsulating project information from clowder.yaml"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.default_ref = None
        self.default_remote = None
        self.groups = []
        self.remotes = []
        self.load_yaml()

    def load_yaml(self):
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

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        names = []
        for group in self.groups:
            names.append(group['name'])
        return names

    def litter(self):
        """Discard changes for all projects"""
        for group in self.groups:
            for project in group.projects:
                project.litter()

    # def sync(self):
    #     """Sync default projects with latest upstream changes"""
    #     self.validate()
    #     for group in self.groups:
    #         if group.name in self.defaults.groups:
    #             for project in group.projects:
    #                 project.sync()

    def sync_all(self):
        """Sync all projects with latest upstream changes"""
        self.validate_all()
        for group in self.groups:
            for project in group.projects:
                project.sync()

    # def sync_version(self, version):
    #     """Sync default projects to fixed versions"""
    #     self.validate()
    #     for group in self.groups:
    #         if group.name in self.defaults.groups:
    #             for project in group.projects:
    #                 project.sync_version(version)

    def sync_version_all(self, version):
        """Sync all projects to fixed versions"""
        self.validate_all()
        for group in self.groups:
            for project in group.projects:
                project.sync_version(version)

    def status(self):
        """Print git status for all projects"""
        clowder_path = os.path.join(self.root_directory, 'clowder')
        git_status(clowder_path, 'clowder')
        print('')
        for group in self.groups:
            for project in group.projects:
                project.status()

    def fix_version(self, version):
        """Fix current commits to versioned clowder.yaml"""
        versions = os.path.join(self.root_directory, 'clowder/versions')
        version_dir = os.path.join(versions, version)
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        if not os.path.exists(yaml_file):
            with open(yaml_file, 'w') as file:
                yaml.dump(self.get_yaml(), file, default_flow_style=False)

    def get_yaml(self):
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

    def get_fixed_version_names(self):
        """Return list of all fixed versions"""
        versions_dir = os.path.join(self.root_directory, 'clowder/versions')
        if os.path.exists(versions_dir):
            return os.listdir(versions_dir)
        return None

    # def validate(self):
    #     """Validate status of default projects"""
    #     for group in self.groups:
    #         if group.name in self.defaults.groups:
    #             for project in group.projects:
    #                 project.validate()

    def validate_all(self):
        """Validate status of all projects"""
        for group in self.groups:
            for project in group.projects:
                project.validate()
