"""clowder.yaml parsing and functionality"""
import os
import sys
from termcolor import cprint
from clowder.group import Group
from clowder.source import Source
from clowder.utility.clowder_utilities import (
    get_yaml_string,
    parse_yaml,
    save_yaml
)
from clowder.utility.clowder_yaml_loading import (
    load_yaml_base,
    load_yaml_import
)
from clowder.utility.clowder_yaml_printing import print_yaml
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
# Disable errors shown by pylint for too many arguments
# pylint: disable=R0913

class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        self._validate_yaml(yaml_file, self._max_import_depth)
        self._load_yaml()

    def branch(self, group_names=None, project_names=None, local=False, remote=False):
        """Show branches"""
        for group in self.groups:
            if project_names is None and group_names is None:
                group.branch(local=local, remote=remote)
            elif project_names is None:
                if group.name in group_names:
                    group.branch(local=local, remote=remote)
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.branch(local=local, remote=remote)

    def clean(self, group_names=None, project_names=None, args=None, recursive=False):
        """Discard changes"""
        for group in self.groups:
            if project_names is None and group_names is None:
                group.clean(args=args, recursive=recursive)
            elif project_names is None:
                if group.name in group_names:
                    group.clean(args=args, recursive=recursive)
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.clean(args=args, recursive=recursive)

    def clean_all(self, group_names=None, project_names=None):
        """Discard all changes"""
        for group in self.groups:
            if project_names is None and group_names is None:
                group.clean_all()
            elif project_names is None:
                if group.name in group_names:
                    group.clean_all()
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.clean_all()

    def diff(self, group_names=None, project_names=None):
        """Show git diff"""
        for group in self.groups:
            if project_names is None and group_names is None:
                group.diff()
            elif project_names is None:
                if group.name in group_names:
                    group.diff()
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.diff()

    def fetch(self, group_names):
        """Fetch groups"""
        for group in self.groups:
            if group.name in group_names:
                group.fetch_all()

    def forall(self, command, ignore_errors, group_names=None, project_names=None):
        """Runs command or script in project directories specified"""
        for group in self.groups:
            if group_names is None and project_names is None:
                for project in group.projects:
                    project.run(command, ignore_errors)
            elif project_names is None:
                if group.name in group_names:
                    for project in group.projects:
                        project.run(command, ignore_errors)
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.run(command, ignore_errors)

    def get_all_fork_project_names(self):
        """Returns all project names containing forks"""
        project_names = []
        for group in self.groups:
            for project in group.projects:
                if project.fork is not None:
                    project_names.append(project.name)
        names = sorted(project_names)
        if not names:
            return ''
        else:
            return names

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        names = sorted([g.name for g in self.groups])
        if names is None:
            return ''
        else:
            return names

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        names = sorted([p.name for g in self.groups for p in g.projects])
        if names is None:
            return ''
        else:
            return names

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml"""
        paths = sorted([p.formatted_project_path() for g in self.groups for p in g.projects])
        if paths is None:
            return ''
        else:
            return paths

    def get_saved_version_names(self):
        """Return list of all saved versions"""
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        if not os.path.exists(versions_dir):
            return None
        versions = os.listdir(versions_dir)
        for version in versions[:]:
            if version.startswith('.'):
                versions.remove(version)
        return versions

    def herd(self, group_names=None, project_names=None, branch=None, depth=None):
        """Sync projects with latest upstream changes"""
        if project_names is None and group_names is None:
            self._validate_groups(self.get_all_group_names())
            for group in self.groups:
                group.herd(branch, depth)
        elif project_names is None:
            self._validate_groups(group_names)
            for group in self.groups:
                if group.name in group_names:
                    group.herd(branch, depth)
        else:
            self._validate_projects(project_names)
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.herd(branch, depth)

    def print_yaml(self, resolved):
        """Print clowder.yaml"""
        if resolved:
            print(get_yaml_string(self._get_yaml_resolved()))
        else:
            print_yaml(self.root_directory)
        sys.exit() # exit early to prevent printing extra newline

    def prune_groups(self, group_names, branch, force=False, local=False, remote=False):
        """Prune branches for groups"""
        self._validate_groups(group_names)
        if local and remote:
            local_branch_exists = self._existing_branch_group(group_names, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_group(group_names, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()
            print(' - Prune local and remote branches\n')
            for group in self.groups:
                if group.name in group_names:
                    group.prune(branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_group(group_names, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()
            for group in self.groups:
                if group.name in group_names:
                    group.prune(branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_group(group_names, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()
            for group in self.groups:
                if group.name in group_names:
                    group.prune(branch, remote=True)

    def prune_projects(self, project_names, branch, force=False, local=False, remote=False):
        """Prune local and remote branch for projects"""
        self._validate_projects(project_names)
        if local and remote:
            self._prune_projects_all(project_names, branch, force)
        elif local:
            if not self._existing_branch_project(project_names, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.prune(branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_project(project_names, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.prune(branch, remote=True)

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
        if os.path.exists(yaml_file):
            print_save_version_exists_error(version_name, yaml_file)
            print()
            sys.exit(1)
        print_save_version(version_name, yaml_file)
        save_yaml(self._get_yaml(), yaml_file)

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

    def stash(self, group_names=None, project_names=None):
        """Stash changes for projects with changes"""
        if not self._is_dirty():
            print('No changes to stash')
            return
        for group in self.groups:
            if project_names is None and group_names is None:
                group.stash()
            elif project_names is None:
                if group.name in group_names:
                    group.stash()
            else:
                for project in group.projects:
                    if project.name in project_names:
                        project.stash()

    def status(self, group_names, padding):
        """Print status for groups"""
        for group in self.groups:
            if group.name in group_names:
                group.status(padding)

    def sync(self, project_names):
        """Print status for groups"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.sync()

    def _existing_branch_group(self, group_names, branch, is_remote):
        """Checks whether at least one branch exists for projects in groups"""
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    if is_remote:
                        if project.existing_branch(branch, is_remote=True):
                            return True
                    else:
                        if project.existing_branch(branch, is_remote=False):
                            return True
        return False

    def _existing_branch_project(self, project_names, branch, is_remote):
        """Checks whether at least one branch exists for projects"""
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    if is_remote:
                        if project.existing_branch(branch, is_remote=True):
                            return True
                    else:
                        if project.existing_branch(branch, is_remote=False):
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

    def _get_yaml_resolved(self):
        """Return python object representation for resolved yaml"""
        groups_yaml = [g.get_yaml_resolved() for g in self.groups]
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
        combined_yaml = {}
        while True:
            if 'import' not in parsed_yaml:
                load_yaml_base(parsed_yaml, combined_yaml)
                break
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
        for parsed_yaml in reversed(imported_yaml_files):
            load_yaml_import(parsed_yaml, combined_yaml)
        self._load_yaml_combined(combined_yaml)

    def _load_yaml_combined(self, combined_yaml):
        """Load clowder from combined yaml"""
        self.defaults = combined_yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0
        self.sources = [Source(s) for s in combined_yaml['sources']]
        for group in combined_yaml['groups']:
            self.groups.append(Group(self.root_directory,
                                     group,
                                     self.defaults,
                                     self.sources))

    def _prune_projects_all(self, project_names, branch, force):
        """Prune local and remote branches for projects"""
        local_branch_exists = self._existing_branch_project(project_names,
                                                            branch, is_remote=False)
        remote_branch_exists = self._existing_branch_project(project_names,
                                                             branch, is_remote=True)
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()
        print(' - Prune local and remote branches\n')
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.prune(branch, force=force, local=True, remote=True)

    def _validate_groups(self, group_names):
        """Validate status of all projects for specified groups"""
        valid = True
        for group in self.groups:
            if group.name in group_names:
                group.print_validation()
                if not group.is_valid():
                    valid = False
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
            print('\n - First run ' + herd_output + ' to clone missing projects\n')
            sys.exit(1)

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
            return
        validate_yaml_import(yaml_file)
        imported_clowder = parsed_yaml['import']
        try:
            if imported_clowder == 'default':
                imported_yaml_file = os.path.join(self.root_directory,
                                                  '.clowder',
                                                  'clowder.yaml')
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
