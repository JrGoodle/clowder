"""clowder.yaml parsing and functionality"""
import os
import sys
from termcolor import cprint
from clowder.group import Group
from clowder.source import Source
from clowder.utility.clowder_utilities import (
    parse_yaml,
    save_yaml
)
from clowder.utility.clowder_yaml_validation import (
    validate_yaml,
    validate_yaml_import
)
from clowder.utility.print_utilities import (
    format_clowder_command,
    format_missing_imported_yaml_error,
    print_error,
    print_invalid_yaml_error,
    print_recursive_import_error,
    print_save_version,
    print_save_version_exists_error
)

# Disable errors shown by pylint for too many public methods
# pylint: disable=R0904
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703

class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.defaults = None
        self.groups = []
        self.sources = []
        self.combined_yaml = {}
        self._max_import_depth = 10

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        self._validate_yaml(yaml_file, self._max_import_depth)
        self._load_yaml()

    def clean_groups(self, group_names):
        """Discard changes for groups"""
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.clean()
        else:
            print(' - No changes to discard')

    def clean_projects(self, project_names):
        """Discard changes for projects"""
        if self._is_dirty():
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.clean()
        else:
            print(' - No changes to discard')

    def diff_groups(self, group_names):
        """Show git diff for groups"""
        for group in self.groups:
            if group.name in group_names:
                group.diff()

    def diff_projects(self, project_names):
        """Show git diff for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.diff()

    def fetch_groups(self, group_names):
        """Print status for groups"""
        for group in self.groups:
            if group.name in group_names:
                group.fetch_all()

    def fetch_projects(self, project_names):
        """Print status for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.fetch_all()

    def forall_groups_run(self, command, group_names, ignore_errors):
        """Runs command or script in all project directories of groups specified"""
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    project.run(command, ignore_errors)

    def forall_projects_run(self, command, project_names, ignore_errors):
        """Runs command or script in all project directories of projects specified"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.run(command, ignore_errors)

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
        self._validate_projects(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.herd(branch, depth)

    def prune_groups_all(self, group_names, branch, force):
        """Prune local and remote branch for groups"""
        self._validate_groups(group_names)
        # print(' - Fetch remote changes\n')
        # self._fetch_groups(group_names)
        # print()
        local_branch_exists = self._existing_branch_group(group_names, branch, is_remote=False)
        remote_branch_exists = self._existing_branch_group(group_names, branch, is_remote=True)
        if local_branch_exists or remote_branch_exists:
            print(' - Prune local and remote branches\n')
            for group in self.groups:
                if group.name in group_names:
                    group.prune_all(branch, force)
        else:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()

    def prune_groups_local(self, group_names, branch, force):
        """Prune local branch for groups"""
        self._validate_groups(group_names)
        if self._existing_branch_group(group_names, branch, is_remote=False):
            for group in self.groups:
                if group.name in group_names:
                    group.prune_local(branch, force)
        else:
            cprint(' - No local branches to prune\n', 'red')
            sys.exit()

    def prune_groups_remote(self, group_names, branch):
        """Prune remote branch for groups"""
        self._validate_groups(group_names)
        # print(' - Fetch remote changes\n')
        # self._fetch_groups(group_names)
        # print()
        if self._existing_branch_group(group_names, branch, is_remote=True):
            for group in self.groups:
                if group.name in group_names:
                    group.prune_remote(branch)
        else:
            cprint(' - No remote branches to prune\n', 'red')
            sys.exit()

    def prune_projects_all(self, project_names, branch, force):
        """Prune local and remote branch for projects"""
        self._validate_projects(project_names)
        # print(' - Fetch remote changes\n')
        # self._fetch_projects(project_names)
        # print()
        local_branch_exists = self._existing_branch_project(project_names, branch, is_remote=False)
        remote_branch_exists = self._existing_branch_project(project_names, branch, is_remote=True)
        if local_branch_exists or remote_branch_exists:
            print(' - Prune local and remote branches\n')
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.prune_all(branch, force)
        else:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()

    def prune_projects_local(self, project_names, branch, force):
        """Prune local branch for projects"""
        self._validate_projects(project_names)
        if self._existing_branch_project(project_names, branch, is_remote=False):
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.prune_local(branch, force)
        else:
            cprint(' - No local branches to prune\n', 'red')
            sys.exit()

    def prune_projects_remote(self, project_names, branch):
        """Prune remote branch for projects"""
        self._validate_projects(project_names)
        # print(' - Fetch remote changes\n')
        # self._fetch_projects(project_names)
        # print()
        if self._existing_branch_project(project_names, branch, is_remote=True):
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.prune_remote(branch)
        else:
            cprint(' - No remote branches to prune\n', 'red')
            sys.exit()

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
        if not os.path.exists(yaml_file):
            print_save_version(version_name, yaml_file)
            save_yaml(self._get_yaml(), yaml_file)
        else:
            print_save_version_exists_error(version_name, yaml_file)
            print()
            sys.exit(1)

    def start_groups(self, group_names, branch, tracking):
        """Start feature branch for groups"""
        self._validate_groups(group_names)
        for group in self.groups:
            if group.name in group_names:
                group.start(branch, tracking)

    def start_projects(self, project_names, branch, tracking):
        """Start feature branch for projects"""
        self._validate_projects(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.start(branch, tracking)

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

    def _existing_branch_group(self, group_names, branch, is_remote):
        """Checks whether at least one branch exists for projects in groups"""
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    if is_remote:
                        if project.existing_remote_branch(branch):
                            return True
                    else:
                        if project.existing_local_branch(branch):
                            return True
        return False

    def _existing_branch_project(self, project_names, branch, is_remote):
        """Checks whether at least one branch exists for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    if is_remote:
                        if project.existing_remote_branch(branch):
                            return True
                    else:
                        if project.existing_local_branch(branch):
                            return True
        return False

    def _fetch_groups(self, group_names):
        """Fetch all projects for specified groups"""
        for group in self.groups:
            if group.name in group_names:
                group.fetch_all()

    def _fetch_projects(self, project_names):
        """Fetch specified projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.fetch_all()

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
        parsed_yaml = parse_yaml(yaml_file)
        imported_yaml_files = []
        while True:
            if 'import' in parsed_yaml:
                imported_yaml_files.append(parsed_yaml)
                imported_yaml = parsed_yaml['import']
                if imported_yaml == 'default':
                    imported_yaml_file = os.path.join(self.root_directory,
                                                      '.clowder',
                                                      'clowder.yaml')
                else:
                    imported_yaml_file = os.path.join(self.root_directory,
                                                      '.clowder',
                                                      'versions',
                                                      imported_yaml,
                                                      'clowder.yaml')
                parsed_yaml = parse_yaml(imported_yaml_file)
                if len(imported_yaml_files) > self._max_import_depth:
                    print_invalid_yaml_error()
                    print_recursive_import_error(self._max_import_depth)
                    print()
                    sys.exit(1)
            else:
                self._load_yaml_base(parsed_yaml)
                break
        for parsed_yaml in reversed(imported_yaml_files):
            self._load_yaml_import(parsed_yaml)
        self._load_yaml_combined()

    def _load_yaml_base(self, parsed_yaml):
        """Load clowder from base yaml file"""
        self.combined_yaml['defaults'] = parsed_yaml['defaults']
        if 'depth' not in parsed_yaml['defaults']:
            self.combined_yaml['defaults']['depth'] = 0
        self.combined_yaml['sources'] = parsed_yaml['sources']
        self.combined_yaml['groups'] = parsed_yaml['groups']

    def _load_yaml_combined(self):
        """Load clowder from combined yaml"""
        self.defaults = self.combined_yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in self.combined_yaml['sources']]

        for group in self.combined_yaml['groups']:
            self.groups.append(Group(self.root_directory,
                                     group,
                                     self.defaults,
                                     self.sources))

    def _load_yaml_import(self, parsed_yaml):
        """Load clowder from import yaml file"""
        if 'defaults' in parsed_yaml:
            imported_defaults = parsed_yaml['defaults']
            if 'ref' in imported_defaults:
                self.combined_yaml['defaults']['ref'] = imported_defaults['ref']
            if 'remote' in imported_defaults:
                self.combined_yaml['defaults']['remote'] = imported_defaults['remote']
            if 'source' in imported_defaults:
                self.combined_yaml['defaults']['source'] = imported_defaults['source']
            if 'depth' in imported_defaults:
                self.combined_yaml['defaults']['depth'] = imported_defaults['depth']

        self._load_yaml_import_sources(parsed_yaml)
        self._load_yaml_import_groups(parsed_yaml)

    def _load_yaml_import_sources(self, parsed_yaml):
        """Load clowder sources from import yaml"""
        if 'sources' in parsed_yaml:
            imported_sources = parsed_yaml['sources']
            source_names = [s['name'] for s in self.combined_yaml['sources']]
            for imported_source in imported_sources:
                if imported_source['name'] in source_names:
                    combined_sources = []
                    for source in self.sources:
                        if source.name == imported_source['name']:
                            combined_sources.append(imported_source)
                        else:
                            combined_sources.append(source)
                    self.combined_yaml['sources'] = combined_sources
                else:
                    self.combined_yaml['sources'].append(imported_source)

    def _load_yaml_import_groups(self, parsed_yaml):
        """Load clowder groups from import yaml"""
        if 'groups' in parsed_yaml:
            imported_groups = parsed_yaml['groups']
            group_names = [g['name'] for g in self.combined_yaml['groups']]
            for imported_group in imported_groups:
                if imported_group['name'] in group_names:
                    combined_groups = []
                    for group in self.combined_yaml['groups']:
                        if group['name'] == imported_group['name']:
                            _load_yaml_import_projects(imported_group,
                                                       group)
                            combined_groups.append(group)
                        else:
                            combined_groups.append(group)
                    self.combined_yaml['groups'] = combined_groups
                else:
                    self.groups.append(imported_group)

    def _validate_groups(self, group_names):
        """Validate status of all projects for specified groups"""
        valid = True
        for group in self.groups:
            if group.name in group_names:
                group.print_validation()
                if not group.is_valid():
                    valid = False
                    break
        if not valid:
            print()
            sys.exit(1)

    def _validate_projects(self, project_names):
        """Validate status of all projects"""
        valid = True
        for project in project_names:
            for group in self.groups:
                for group_project in group.projects:
                    if group_project.name == project:
                        if not group_project.is_valid():
                            valid = False
                            break
        if not valid:
            print()
            sys.exit(1)

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups"""
        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.projects_exist():
                projects_exist = False
        if not projects_exist:
            herd_output = format_clowder_command('clowder herd')
            print()
            print(' - First run ' + herd_output + ' to clone missing projects')
            print()
            sys.exit(1)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104

    def _validate_yaml(self, yaml_file, max_import_depth):
        """Validate clowder.yaml"""
        parsed_yaml = parse_yaml(yaml_file)
        if max_import_depth < 0:
            print_invalid_yaml_error()
            print_recursive_import_error(self._max_import_depth)
            print()
            sys.exit(1)
        if 'import' not in parsed_yaml:
            validate_yaml(yaml_file)
        else:
            validate_yaml_import(yaml_file)
            imported_clowder = parsed_yaml['import']
            try:
                if imported_clowder == 'default':
                    imported_yaml_file = os.path.join(self.root_directory,
                                                      '.clowder',
                                                      'clowder.yaml')
                    if not os.path.isfile(imported_yaml_file):
                        error = format_missing_imported_yaml_error(imported_yaml_file,
                                                                   yaml_file)
                        raise Exception(error)
                else:
                    imported_yaml_file = os.path.join(self.root_directory,
                                                      '.clowder',
                                                      'versions',
                                                      imported_clowder,
                                                      'clowder.yaml')
                    if not os.path.isfile(imported_yaml_file):
                        error = format_missing_imported_yaml_error(imported_yaml_file,
                                                                   yaml_file)
                        raise Exception(error)
                yaml_file = imported_yaml_file
            except Exception as err:
                print_invalid_yaml_error()
                print_error(err)
                sys.exit(1)
            self._validate_yaml(yaml_file, max_import_depth - 1)

def _load_yaml_import_projects(imported_group, group):
    """Load clowder projects from imported group"""
    project_names = [p['name'] for p in group['projects']]
    for imported_project in imported_group['projects']:
        if imported_project['name'] in project_names:
            combined_projects = []
            for project in group['projects']:
                if project.name == imported_project['name']:
                    if 'path' not in imported_project:
                        imported_project['path'] = project['path']

                    if 'depth' not in imported_project:
                        imported_project['depth'] = project['depth']

                    if 'ref' not in imported_project:
                        imported_project['ref'] = project['ref']

                    if 'remote' not in imported_project:
                        imported_project['remote'] = project['remote_name']

                    if 'source' not in imported_project:
                        imported_project['source'] = project['source']['name']

                    combined_project = imported_project
                    combined_projects.append(combined_project)
                else:
                    combined_projects.append(project)
            group['projects'] = combined_projects
        else:
            combined_project = imported_project
            group['projects'].append(combined_project)
