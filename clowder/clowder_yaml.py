"""clowder.yaml parsing and functionality"""
import os
import yaml

from clowder.defaults import Defaults
from clowder.group import Group
from clowder.remote import Remote

class ClowderYAML(object):
    """Class encapsulating project information from clowder.yaml"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory

        self.defaults = None
        self.groups = []
        self.remotes = []

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.exists(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)

                self.defaults = Defaults(parsed_yaml['defaults'])

                for remote in parsed_yaml['remotes']:
                    self.remotes.append(Remote(remote))

                for group in parsed_yaml['groups']:
                    self.groups.append(Group(self.root_directory,
                                             group,
                                             self.defaults,
                                             self.remotes))

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        names = []
        for group in self.groups:
            names.append(group['name'])
        return names

    def sync(self):
        """Sync all projects with latest upstream changes"""
        for group in self.groups:
            for project in group.projects:
                project.sync()

    def sync_version(self, version):
        """Sync all projects to fixed versions"""
        for group in self.groups:
            for project in group.projects:
                project.sync_version(version)

    def status(self):
        """Print git status for all projects"""
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

        return {'defaults': self.defaults.get_yaml(),
                'remotes': remotes_yaml,
                'groups': groups_yaml}
