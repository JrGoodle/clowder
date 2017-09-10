"""clowder.yaml parsing and functionality"""
import os
import sys
import yaml
from termcolor import colored
from clowder.group import Group
from clowder.project import Project
from clowder.source import Source
from clowder.utility.clowder_utilities import (
    validate_yaml,
    validate_yaml_import
)

# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.defaults = None
        self.groups = []
        self.sources = []

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.isfile(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = _parse_yaml(file)
        else:
            print('')
            clowder_output = colored('clowder.yaml', 'cyan')
            print(clowder_output + ' appears to be missing')
            print('')
            sys.exit(1)
        self._validate_yaml(parsed_yaml)
        self._load_yaml()

    def clean_groups(self, group_names):
        """Discard changes for groups"""
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.clean()
        else:
            print('No changes to discard')

    def clean_projects(self, project_names):
        """Discard changes for projects"""
        if self._is_dirty():
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.clean()
        else:
            print('No changes to discard')

    def fetch_groups(self, group_names):
        """Print status for groups"""
        for group in self.groups:
            if group.name in group_names:
                group.fetch()

    def fetch_projects(self, project_names):
        """Print status for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.fetch()

    def forall_groups_run(self, command, group_names, ignore_errors):
        """Runs command or script in all project directories of groups specified"""
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    project.run(command, ignore_errors)
        sys.exit() # Exit early to prevent printing extra newline

    def forall_projects_run(self, command, project_names, ignore_errors):
        """Runs command or script in all project directories of projects specified"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.run(command, ignore_errors)
        sys.exit() # Exit early to prevent printing extra newline

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        return sorted([g.name for g in self.groups])

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        return sorted([p.name for g in self.groups for p in g.projects])

    def get_saved_version_names(self):
        """Return list of all saved versions"""
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        if os.path.exists(versions_dir):
            versions = os.listdir(versions_dir)
            for version in versions[:]:
                if version.startswith('.'):
                    versions.remove(version)
            return versions
        else:
            return None

    def herd_groups(self, group_names, branch=None, depth=None):
        """Sync groups with latest upstream changes"""
        self._validate_groups(group_names)
        for group in self.groups:
            if group.name in group_names:
                group.herd(branch, depth)

    def herd_projects(self, project_names, branch=None, depth=None):
        """Sync projects with latest upstream changes"""
        self._validate_groups(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.herd(branch, depth)

    def prune_groups(self, group_names, branch, is_remote, force):
        """Prune branch for groups"""
        self._validate_groups(group_names)
        for group in self.groups:
            if group.name in group_names:
                group.prune(branch, is_remote, force)

    def prune_projects(self, project_names, branch, is_remote, force):
        """Prune branch for projects"""
        self._validate_groups(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.prune(branch, is_remote, force)

    def save_version(self, version):
        """Save current commits to a clowder.yaml in the versions directory"""
        self._validate_projects_exist()
        self._validate_groups(self.get_all_group_names())
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        version_name = version.replace('/', '-') # Replace path separateors with dashes
        version_dir = os.path.join(versions_dir, version_name)
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        yaml_file_output = colored(yaml_file, 'cyan')
        version_output = colored(version_name, attrs=['bold'])
        if not os.path.exists(yaml_file):
            with open(yaml_file, 'w') as file:
                print('Saving version ' + version_output + ' at ' + yaml_file_output)
                yaml.dump(self._get_yaml(), file, default_flow_style=False)
        else:
            print('Version ' + version_output + ' already exists at ' + yaml_file_output)
            sys.exit(1)

    def start_groups(self, group_names, branch):
        """Start feature branch for groups"""
        self._validate_groups(group_names)
        for group in self.groups:
            if group.name in group_names:
                group.start(branch)

    def start_projects(self, project_names, branch):
        """Start feature branch for projects"""
        self._validate_groups(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.start(branch)

    def stash_groups(self, group_names):
        """Stash changes for groups with changes"""
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.stash()
        else:
            print('No changes to stash')

    def stash_projects(self, project_names):
        """Stash changes for projects with changes"""
        if self._is_dirty():
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.stash()
        else:
            print('No changes to stash')

    def status_groups(self, group_names, verbose=False):
        """Print status for groups"""
        for group in self.groups:
            if group.name in group_names:
                if verbose is False:
                    group.status()
                else:
                    group.status_verbose()

    def status_projects(self, project_names, verbose=False):
        """Print status for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    if verbose is False:
                        project.status()
                    else:
                        project.status_verbose()

    def _get_yaml(self):
        """Return python object representation for saving yaml"""
        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
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
        if os.path.isfile(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = _parse_yaml(file)
                imported_yaml_files = []
                while True:
                    if 'import' in parsed_yaml:
                        imported_yaml = parsed_yaml['import']
                        if imported_yaml == 'default':
                            imported_yaml_file = yaml_file = os.path.join(self.root_directory,
                                                                          '.clowder',
                                                                          'clowder.yaml')
                        else:
                            imported_yaml_file = yaml_file = os.path.join(self.root_directory,
                                                                          '.clowder',
                                                                          'versions',
                                                                          imported_yaml,
                                                                          'clowder.yaml')
                        if os.path.isfile(imported_yaml_file):
                            with open(imported_yaml_file) as file:
                                parsed_imported_yaml = _parse_yaml(file)
                                imported_yaml_files.append(parsed_imported_yaml)
                                parsed_yaml = parsed_imported_yaml
                        else:
                            print('')
                            clowder_output = colored('clowder.yaml', 'cyan')
                            print(clowder_output + ' appears to be missing')
                            print('')
                            sys.exit(1)
                        if len(imported_yaml_files) > 10:
                            print('')
                            clowder_output = colored('clowder.yaml', 'cyan')
                            print(clowder_output + ' has too many recursive imports')
                            print('Currently the max is 10')
                            print('')
                            sys.exit(1)
                    else:
                        self._load_yaml_base(parsed_yaml)
                        break
                for parsed_yaml in reversed(imported_yaml_files):
                    self._load_yaml_import(parsed_yaml)

    def _load_yaml_base(self, parsed_yaml):
        """Load clowder from base yaml file"""
        self.defaults = parsed_yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in parsed_yaml['sources']]

        for group in parsed_yaml['groups']:
            self.groups.append(Group(self.root_directory,
                                     group,
                                     self.defaults,
                                     self.sources))

    def _load_yaml_import(self, parsed_yaml):
        """Load clowder from import yaml file"""
        if 'defaults' in parsed_yaml:
            imported_defaults = parsed_yaml['defaults']
            if 'ref' in imported_defaults:
                self.defaults['ref'] = imported_defaults['ref']
            if 'remote' in imported_defaults:
                self.defaults['remote'] = imported_defaults['remote']
            if 'source' in imported_defaults:
                self.defaults['source'] = imported_defaults['source']
            if 'depth' in imported_defaults:
                self.defaults['depth'] = imported_defaults['depth']

        self._load_yaml_import_sources(parsed_yaml)
        self._load_yaml_import_groups(parsed_yaml)

    def _load_yaml_import_sources(self, parsed_yaml):
        """Load clowder sources from import yaml"""
        if 'sources' in parsed_yaml:
            imported_sources = parsed_yaml['sources']
            source_names = [s.name for s in self.sources]
            for imported_source in imported_sources:
                if imported_source['name'] in source_names:
                    combined_sources = []
                    for source in self.sources:
                        if source.name == imported_source['name']:
                            combined_sources.append(Source(imported_source))
                        else:
                            combined_sources.append(source)
                    self.sources = combined_sources
                else:
                    self.sources.append(imported_source)

    def _load_yaml_import_groups(self, parsed_yaml):
        """Load clowder groups from import yaml"""
        if 'groups' in parsed_yaml:
            imported_groups = parsed_yaml['groups']
            group_names = [g.name for g in self.groups]
            for imported_group in imported_groups:
                if imported_group['name'] in group_names:
                    combined_groups = []
                    for group in self.groups:
                        if group.name == imported_group['name']:
                            imp_group = Group(self.root_directory,
                                              imported_group,
                                              self.defaults,
                                              self.sources)
                            combined_group = self._load_yaml_import_projects(imp_group,
                                                                             group)
                            combined_groups.append(combined_group)
                        else:
                            combined_groups.append(group)
                    self.groups = combined_groups
                else:
                    self.groups.append(Group(self.root_directory,
                                             imported_group,
                                             self.defaults,
                                             self.sources))

    def _load_yaml_import_projects(self, imported_group, group):
        """Load clowder projects from imported group"""
        project_names = [p.name for p in group.projects]
        for imported_project in imported_group.projects:
            if imported_project.name in project_names:
                combined_projects = []
                for project in group.projects:
                    if project.name == imported_project.name:
                        if 'path' not in imported_project:
                            imported_project['path'] = project.path

                        if 'depth' not in imported_project:
                            imported_project['depth'] = project.depth

                        if 'ref' not in imported_project:
                            imported_project['ref'] = project.ref

                        if 'remote' not in imported_project:
                            imported_project['remote'] = project.remote_name

                        if 'source' not in imported_project:
                            imported_project['source'] = project.source['name']

                        combined_project = Project(self.root_directory,
                                                   imported_project,
                                                   self.defaults,
                                                   self.sources)
                        combined_projects.append(combined_project)
                    else:
                        combined_projects.append(project)
                group.projects = combined_projects
            else:
                combined_project = Project(self.root_directory,
                                           imported_project,
                                           self.defaults,
                                           self.sources)
                group.projects.append(combined_project)

    def _validate_groups(self, group_names):
        """Validate status of all projects for specified groups"""
        valid = True
        for group in self.groups:
            if group.name in group_names:
                group.print_validation()
                if not group.is_valid():
                    valid = False
        if not valid:
            print('')
            sys.exit(1)

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups"""
        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.projects_exist():
                projects_exist = False
        if not projects_exist:
            herd_output = colored('clowder herd', 'yellow')
            print('')
            print('First run ' + herd_output + ' to clone missing projects')
            sys.exit(1)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104

    def _validate_yaml(self, parsed_yaml):
        """Validate clowder.yaml"""
        if 'import' not in parsed_yaml:
            validate_yaml(parsed_yaml)
        else:
            validate_yaml_import(parsed_yaml)
            imported_clowder = parsed_yaml['import']
            try:
                if imported_clowder == 'default':
                    yaml_file = os.path.join(self.root_directory,
                                             '.clowder',
                                             'clowder.yaml')
                    if not os.path.isfile(clowder_yaml):
                        error_message = colored('Missing imported clowder.yaml\n', 'red')
                        error = error_message + path + '\n'
                        raise Exception('Missing clowder.yaml')
                else:
                    yaml_file = os.path.join(self.root_directory,
                                             '.clowder',
                                             'versions',
                                             imported_clowder,
                                             'clowder.yaml')
                    if not os.path.isfile(clowder_yaml):
                        error_message = colored('Missing imported clowder.yaml\n', 'red')
                        error = error_message + path + '\n'
                        raise Exception('Missing clowder.yaml')
            except:
                print('')
                clowder_output = colored('clowder.yaml', 'cyan')
                print(clowder_output + ' appears to be invalid')
                print('')
                print(error)
                sys.exit(1)
            with open(yaml_file) as file:
                parsed_yaml_import = _parse_yaml(file)
                self._validate_yaml(parsed_yaml_import)

def _parse_yaml(yaml_file):
    """Parse yaml file"""
    parsed_yaml = yaml.safe_load(yaml_file)
    if parsed_yaml is None:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        print(colored('clowder.yaml has no elements\n', 'red'))
    else:
        return parsed_yaml
