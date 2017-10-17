"""clowder.yaml parsing and functionality"""

from __future__ import print_function
import os
import sys
from termcolor import cprint
from clowder.group import Group
from clowder.source import Source
from clowder.exception.clowder_exception import ClowderException
from clowder.utility.clowder_pool import ClowderPool
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
    format_command,
    format_fork_string,
    format_missing_imported_yaml_error,
    print_error,
    print_invalid_yaml_error,
    print_recursive_import_error,
    print_save_version,
    print_save_version_exists_error
)


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10
        self._pool = None

        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        self._validate_yaml(yaml_file, self._max_import_depth)
        self._load_yaml()

    def branch(self, group_names=None, project_names=None, local=False, remote=False):
        """Show branches"""
        if project_names is None and group_names is None:
            for group in self.groups:
                group.branch(local=local, remote=remote)
        elif project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.branch(local=local, remote=remote)
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                project.branch(local=local, remote=remote)

    def clean(self, group_names=None, project_names=None, args='', recursive=False):
        """Discard changes"""
        if project_names is None and group_names is None:
            for group in self.groups:
                group.clean(args=args, recursive=recursive)
        elif project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.clean(args=args, recursive=recursive)
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                project.clean(args=args, recursive=recursive)

    def clean_all(self, group_names=None, project_names=None):
        """Discard all changes"""
        if project_names is None and group_names is None:
            for group in self.groups:
                group.clean_all()
        elif project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.clean_all()
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                project.clean_all()

    def diff(self, group_names=None, project_names=None):
        """Show git diff"""
        if project_names is None and group_names is None:
            for group in self.groups:
                group.diff()
        elif project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            if group in groups:
                group.diff()
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                project.diff()

    def fetch(self, group_names):
        """Fetch groups"""
        for group in self.groups:
            if group.name in group_names:
                group.fetch_all()

    def forall(self, command, ignore_errors, group_names=None, project_names=None, parallel=False):
        """Runs command or script in project directories specified"""
        if parallel:
            self._pool = ClowderPool()
        if group_names is None and project_names is None:
            projects = [p for g in self.groups for p in g.projects]
        elif project_names is None:
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            if parallel:
                project.print_status()
                if not os.path.isdir(project.full_path()):
                    cprint(" - Project is missing\n", 'red')
                    continue
                print(format_command(command))
            project.run(command, ignore_errors, pool=self._pool)
        if self._pool is not None:
            self._pool.close()
            self._pool.join()

    def get_all_fork_project_names(self):
        """Returns all project names containing forks"""
        project_names = sorted([p.name for g in self.groups for p in g.projects if p.fork is not None])
        if not project_names:
            return ''
        return project_names

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        names = sorted([g.name for g in self.groups])
        if names is None:
            return ''
        return names

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        names = sorted([p.name for g in self.groups for p in g.projects])
        if names is None:
            return ''
        return names

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml"""
        paths = sorted([p.formatted_project_path() for g in self.groups for p in g.projects])
        if paths is None:
            return ''
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

    def herd(self, group_names=None, project_names=None, branch=None, tag=None,
             depth=None, rebase=False, parallel=False):
        """Pull or rebase latest upstream changes for projects"""
        if parallel:
            self._pool = ClowderPool()
        if project_names is None and group_names is None:
            self._validate_groups(self.get_all_group_names())
            for group in self.groups:
                group.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, pool=self._pool)
        elif project_names is None:
            self._validate_groups(group_names)
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, pool=self._pool)
        else:
            self._validate_projects(project_names)
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                if parallel:
                    project.print_status()
                    if project.fork is not None:
                        print(format_fork_string(project.name))
                        print(format_fork_string(project.fork.name))
                project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, pool=self._pool)
        if self._pool is not None:
            self._pool.close()
            self._pool.join()

    def print_yaml(self, resolved):
        """Print clowder.yaml"""
        if resolved:
            print(get_yaml_string(self._get_yaml_resolved()))
        else:
            print_yaml(self.root_directory)
        sys.exit()  # exit early to prevent printing extra newline

    def prune_groups(self, group_names, branch, force=False, local=False, remote=False):
        """Prune branches for groups"""
        self._validate_groups(group_names)
        groups = [g for g in self.groups if g.name in group_names]
        if local and remote:
            local_branch_exists = self._existing_branch_group(group_names, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_group(group_names, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()
            print(' - Prune local and remote branches\n')
            for group in groups:
                group.prune(branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_group(group_names, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()
            for group in groups:
                group.prune(branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_group(group_names, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()
            for group in groups:
                group.prune(branch, remote=True)

    def prune_projects(self, project_names, branch, force=False, local=False, remote=False):
        """Prune local and remote branch for projects"""
        self._validate_projects(project_names)
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        if local and remote:
            self._prune_projects_all(project_names, branch, force)
        elif local:
            if not self._existing_branch_project(project_names, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()
            for project in projects:
                project.prune(branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_project(project_names, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()
            for project in projects:
                project.prune(branch, remote=True)

    def reset(self, group_names=None, project_names=None, parallel=False):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD"""
        if parallel:
            self._pool = ClowderPool()
        if project_names is None and group_names is None:
            self._validate_groups(self.get_all_group_names())
            for group in self.groups:
                group.reset(pool=self._pool)
        elif project_names is None:
            self._validate_groups(group_names)
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.reset(pool=self._pool)
        else:
            self._validate_projects(project_names)
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                if parallel:
                    project.print_status()
                    if project.fork is not None:
                        print(format_fork_string(project.name))
                        print(format_fork_string(project.fork.name))
                project.reset(pool=self._pool)
        if self._pool is not None:
            self._pool.close()
            self._pool.join()

    def save_version(self, version):
        """Save current commits to a clowder.yaml in the versions directory"""
        self._validate_projects_exist()
        self._validate_groups(self.get_all_group_names())
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        version_name = version.replace('/', '-')  # Replace path separators with dashes
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
        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.start(branch, tracking)

    def start_projects(self, project_names, branch, tracking):
        """Start feature branch for projects"""
        self._validate_projects(project_names)
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            project.start(branch, tracking)

    def stash(self, group_names=None, project_names=None):
        """Stash changes for projects with changes"""
        if not self._is_dirty():
            print('No changes to stash')
            return
        if project_names is None and group_names is None:
            for group in self.groups:
                group.stash()
        elif project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                group.stash()
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]
            for project in projects:
                project.stash()

    def status(self, group_names, padding):
        """Print status for groups"""
        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.status(padding)

    def sync(self, project_names, rebase=False, parallel=False):
        """Sync projects"""
        if parallel:
            self._pool = ClowderPool()
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            if parallel:
                project.print_status()
                if project.fork is not None:
                    print(format_fork_string(project.name))
                    print(format_fork_string(project.fork.name))
            project.sync(rebase=rebase, pool=self._pool)
        if self._pool is not None:
            self._pool.close()
            self._pool.join()

    def _existing_branch_group(self, group_names, branch, is_remote):
        """Checks whether at least one branch exists for projects in groups"""
        projects = [p for g in self.groups if g.name in group_names for p in g.projects]
        for project in projects:
            if is_remote:
                if project.existing_branch(branch, is_remote=True):
                    return True
            else:
                if project.existing_branch(branch, is_remote=False):
                    return True
        return False

    def _existing_branch_project(self, project_names, branch, is_remote):
        """Checks whether at least one branch exists for projects"""
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            if is_remote:
                if project.existing_branch(branch, is_remote=True):
                    return True
            else:
                if project.existing_branch(branch, is_remote=False):
                    return True
        return False

    def _fetch_groups(self, group_names):
        """Fetch all projects for specified groups"""
        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.fetch_all()

    def _fetch_projects(self, project_names):
        """Fetch specified projects"""
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
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
        return any([g.is_dirty() for g in self.groups])

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
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_yaml, 'clowder.yaml')
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
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))

    def _prune_projects_all(self, project_names, branch, force):
        """Prune local and remote branches for projects"""
        local_branch_exists = self._existing_branch_project(project_names, branch, is_remote=False)
        remote_branch_exists = self._existing_branch_project(project_names, branch, is_remote=True)
        branch_exists = local_branch_exists or remote_branch_exists
        if not branch_exists:
            cprint(' - No local or remote branches to prune\n', 'red')
            sys.exit()
        print(' - Prune local and remote branches\n')
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            project.prune(branch, force=force, local=True, remote=True)

    def _validate_groups(self, group_names):
        """Validate status of all projects for specified groups"""
        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            group.print_validation()
        if not all([g.is_valid() for g in groups]):
            print()
            sys.exit(1)

    def _validate_projects(self, project_names):
        """Validate status of all projects"""
        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        if not all([p.is_valid() for p in projects]):
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
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_clowder, 'clowder.yaml')
            if not os.path.isfile(imported_yaml_file):
                error = format_missing_imported_yaml_error(imported_yaml_file, yaml_file)
                raise ClowderException(error)
            yaml_file = imported_yaml_file
        except ClowderException as err:
            print_invalid_yaml_error()
            print_error(err)
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        self._validate_yaml(yaml_file, max_import_depth - 1)
