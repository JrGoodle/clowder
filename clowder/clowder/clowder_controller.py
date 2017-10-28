"""clowder.yaml parsing and functionality"""

from __future__ import print_function

import multiprocessing as mp
import os
import signal
import sys

import psutil
from termcolor import cprint

import clowder.util.formatting as fmt
import clowder.util.clowder_yaml as clowder_yaml
from clowder.error.clowder_error import ClowderError
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.util.progress import Progress


def herd_project(project, branch, tag, depth, rebase):
    """Clone project or update latest from upstream"""

    project.herd(branch=branch, tag=tag, depth=depth, rebase=rebase, parallel=True)


def reset_project(project, timestamp):
    """Reset project branches to upstream or checkout tag/sha as detached HEAD"""

    project.reset(timestamp=timestamp, parallel=True)


def run_project(project, command, ignore_errors):
    """Run command or script in project directory"""

    project.run(command, ignore_errors, parallel=True)


def sync_project(project, rebase):
    """Sync fork project with upstream"""

    project.sync(rebase, parallel=True)


def async_callback(val):
    """Increment async progress bar"""

    del val
    __clowder_progress__.update()


__clowder_parent_id__ = os.getpid()


def worker_init():
    """
    Process pool terminator
    Adapted from https://stackoverflow.com/a/45259908
    """

    def sig_int(signal_num, frame):
        """Signal handler"""

        del signal_num, frame
        parent = psutil.Process(__clowder_parent_id__)
        for child in parent.children(recursive=True):
            if child.pid != os.getpid():
                child.terminate()
        parent.terminate()
        psutil.Process(os.getpid()).terminate()
        print('\n\n')

    signal.signal(signal.SIGINT, sig_int)


__clowder_results__ = []
__clowder_pool__ = mp.Pool(initializer=worker_init)
__clowder_progress__ = Progress()


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10
        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        self._validate_yaml(yaml_file, self._max_import_depth)
        self._load_yaml()

    def branch(self, group_names, project_names=None, skip=None, local=False, remote=False):
        """Show branches"""

        if skip is None:
            skip = []

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'branch', local=local, remote=remote)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'branch', local=local, remote=remote)

    def clean(self, group_names, project_names=None, skip=None, args='', recursive=False):
        """Discard changes"""

        if skip is None:
            skip = []

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'clean', args=args, recursive=recursive)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'clean', args=args, recursive=recursive)

    def clean_all(self, group_names, skip=None, project_names=None):
        """Discard all changes"""

        if skip is None:
            skip = []

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'clean_all')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'clean_all')

    def diff(self, group_names, project_names=None):
        """Show git diff"""

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, [], 'diff')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            print(project.status())
            project.diff()

    def fetch(self, group_names):
        """Fetch groups"""

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            self._run_group_command(group, [], 'fetch_all')

    def forall(self, command, ignore_errors, group_names, project_names=None, skip=None, parallel=False):
        """Runs command or script in project directories specified"""

        if skip is None:
            skip = []

        if project_names is None:
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
        else:
            projects = [p for g in self.groups for p in g.projects if p.name in project_names]

        if parallel:
            self._forall_parallel(command, skip, ignore_errors, projects)
            return

        for project in projects:
            self._run_project_command(project, skip, 'run', command, ignore_errors)

    def get_all_fork_project_names(self):
        """Returns all project names containing forks"""

        project_names = sorted([p.name for g in self.groups for p in g.projects if p.fork])
        return '' if project_names is None else project_names

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""

        names = sorted([g.name for g in self.groups])
        return '' if names is None else names

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""

        names = sorted([p.name for g in self.groups for p in g.projects])
        return '' if names is None else names

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml"""

        paths = sorted([p.formatted_project_path() for g in self.groups for p in g.projects])
        return '' if paths is None else paths

    def get_saved_version_names(self):
        """Return list of all saved versions"""

        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        if not os.path.exists(versions_dir):
            return None
        return [v for v in os.listdir(versions_dir) if not v.startswith('.') if v.lower() != 'default']

    def herd(self, group_names, project_names=None, skip=None, branch=None, tag=None, depth=None, rebase=False):
        """Pull or rebase latest upstream changes for projects"""

        if skip is None:
            skip = []

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            for group in groups:
                self._run_group_command(group, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)

    def herd_parallel(self, group_names, project_names=None, skip=None, branch=None, tag=None,
                      depth=None, rebase=False):
        """Pull or rebase latest upstream changes for projects in parallel"""

        if skip is None:
            skip = []

        print(' - Herd projects in parallel\n')
        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
            self._print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                      callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(herd_project, args=(project, branch, tag, depth, rebase),
                                                  callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    def print_yaml(self, resolved):
        """Print clowder.yaml"""

        if resolved:
            print(fmt.yaml_string(self._get_yaml_resolved()))
        else:
            clowder_yaml.print_yaml(self.root_directory)
        sys.exit()  # exit early to prevent printing extra newline

    def prune(self, group_names, branch, project_names=None, skip=None, force=False, local=False, remote=False):
        """Prune branches"""

        if skip is None:
            skip = []

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            self._prune_groups(groups, branch, skip=skip, force=force, local=local, remote=remote)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._prune_projects(projects, branch, skip=skip, force=force, local=local, remote=remote)

    def reset(self, group_names, project_names=None, skip=None, timestamp_project=None, parallel=False):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD"""

        if skip is None:
            skip = []

        if parallel:
            self._reset_parallel(group_names, skip=skip, timestamp_project=timestamp_project)
            return

        timestamp = None
        if timestamp_project:
            timestamp = self._get_timestamp(timestamp_project)
        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            for group in groups:
                self._run_group_command(group, skip, 'reset', timestamp=timestamp)
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'reset', timestamp=timestamp)

    def save_version(self, version):
        """Save current commits to a clowder.yaml in the versions directory"""

        self._validate_projects_exist()
        self._validate_groups(self.groups)
        versions_dir = os.path.join(self.root_directory, '.clowder', 'versions')
        version_name = version.replace('/', '-')  # Replace path separators with dashes
        version_dir = os.path.join(versions_dir, version_name)
        if not os.path.exists(version_dir):
            try:
                os.makedirs(version_dir)
            except OSError as err:
                if err.errno != os.errno.EEXIST:
                    raise

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        if os.path.exists(yaml_file):
            print(fmt.save_version_exists_error(version_name, yaml_file))
            print()
            sys.exit(1)

        print(fmt.save_version(version_name, yaml_file))
        clowder_yaml.save_yaml(self._get_yaml(), yaml_file)

    def start_groups(self, group_names, skip, branch, tracking=False):
        """Start feature branch for groups"""

        groups = [g for g in self.groups if g.name in group_names]
        self._validate_groups(groups)
        for group in groups:
            self._run_group_command(group, skip, 'start', branch, tracking)

    def start_projects(self, project_names, skip, branch, tracking=False):
        """Start feature branch for projects"""

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        for project in projects:
            self._run_project_command(project, skip, 'start', branch, tracking)

    def stash(self, group_names, skip=None, project_names=None):
        """Stash changes for projects with changes"""

        if skip is None:
            skip = []

        if not self._is_dirty():
            print('No changes to stash')
            return

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            for group in groups:
                self._run_group_command(group, skip, 'stash')
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        for project in projects:
            self._run_project_command(project, skip, 'stash')

    def status(self, group_names, padding):
        """Print status for groups"""

        groups = [g for g in self.groups if g.name in group_names]
        for group in groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                print(project.status(padding=padding))

    def sync(self, project_names, rebase=False, parallel=False):
        """Sync projects"""

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        if parallel:
            self._sync_parallel(projects, rebase=rebase)
            return

        for project in projects:
            project.sync(rebase=rebase)

    @staticmethod
    def _existing_branch_groups(groups, branch, is_remote):
        """Checks whether at least one branch exists for projects in groups"""

        return any([p.existing_branch(branch, is_remote=is_remote) for g in groups for p in g.projects])

    @staticmethod
    def _existing_branch_projects(projects, branch, is_remote):
        """Checks whether at least one branch exists for projects"""

        return any([p.existing_branch(branch, is_remote=is_remote) for p in projects])

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

    @staticmethod
    def _forall_parallel(command, skip, ignore_errors, projects):
        """Runs command or script in project directories specified"""

        print(' - Run forall commands in parallel\n')
        for project in projects:
            if project.name in skip:
                continue
            print(project.status())
            if not os.path.isdir(project.full_path()):
                cprint(" - Project is missing", 'red')

        print('\n' + fmt.command(command))
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(run_project, args=(project, command, ignore_errors),
                                                  callback=async_callback)
            __clowder_results__.append(result)

        pool_handler(len(projects))

    def _get_timestamp(self, timestamp_project):
        """Return timestamp for project"""

        timestamp = None
        all_projects = [p for g in self.groups for p in g.projects]
        for project in all_projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            cprint(' - Failed to find timestamp\n', 'red')
            sys.exit(1)

        return timestamp

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
        parsed_yaml = clowder_yaml.parse_yaml(yaml_file)
        imported_yaml_files = []
        combined_yaml = {}
        while True:
            if 'import' not in parsed_yaml:
                clowder_yaml.load_yaml_base(parsed_yaml, combined_yaml)
                break
            imported_yaml_files.append(parsed_yaml)
            imported_yaml = parsed_yaml['import']

            if imported_yaml == 'default':
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_yaml, 'clowder.yaml')

            parsed_yaml = clowder_yaml.parse_yaml(imported_yaml_file)
            if len(imported_yaml_files) > self._max_import_depth:
                print(fmt.invalid_yaml_error())
                print(fmt.recursive_import_error(self._max_import_depth))
                print()
                sys.exit(1)

        for parsed_yaml in reversed(imported_yaml_files):
            clowder_yaml.load_yaml_import(parsed_yaml, combined_yaml)

        self._load_yaml_combined(combined_yaml)

    def _load_yaml_combined(self, combined_yaml):
        """Load clowder from combined yaml"""

        self.defaults = combined_yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in combined_yaml['sources']]
        for group in combined_yaml['groups']:
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))

    @staticmethod
    def _print_parallel_groups_output(groups, skip):
        """Print output for parallel group command"""

        for group in groups:
            print(fmt.group_name(group.name))
            for project in group.projects:
                if project.name in skip:
                    continue
                print(project.status())
                if project.fork:
                    print('  ' + fmt.fork_string(project.name))
                    print('  ' + fmt.fork_string(project.fork.name))

    @staticmethod
    def _print_parallel_projects_output(projects, skip):
        """Print output for parallel project command"""

        for project in projects:
            if project.name in skip:
                continue
            print(project.status())
            if project.fork:
                print('  ' + fmt.fork_string(project.name))
                print('  ' + fmt.fork_string(project.fork.name))

    def _prune_groups(self, groups, branch, skip=None, force=False, local=False, remote=False):
        """Prune group branches"""

        if local and remote:
            local_branch_exists = self._existing_branch_groups(groups, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_groups(groups, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()

            print(' - Prune local and remote branches\n')
            for group in groups:
                local_branch_exists = group.existing_branch(branch, is_remote=False)
                remote_branch_exists = group.existing_branch(branch, is_remote=True)
                if local_branch_exists or remote_branch_exists:
                    self._run_group_command(group, skip, 'prune', branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_groups(groups, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()

            for group in groups:
                if group.existing_branch(branch, is_remote=False):
                    self._run_group_command(group, skip, 'prune', branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_groups(groups, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()

            for group in groups:
                if group.existing_branch(branch, is_remote=True):
                    self._run_group_command(group, skip, 'prune', branch, remote=True)

    def _prune_projects(self, projects, branch, skip=None, force=False, local=False, remote=False):
        """Prune project branches"""

        if local and remote:
            local_branch_exists = self._existing_branch_projects(projects, branch, is_remote=False)
            remote_branch_exists = self._existing_branch_projects(projects, branch, is_remote=True)
            branch_exists = local_branch_exists or remote_branch_exists
            if not branch_exists:
                cprint(' - No local or remote branches to prune\n', 'red')
                sys.exit()

            print(' - Prune local and remote branches\n')
            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, force=force, local=True, remote=True)
        elif local:
            if not self._existing_branch_projects(projects, branch, is_remote=False):
                print(' - No local branches to prune\n')
                sys.exit()

            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, force=force, local=True)
        elif remote:
            if not self._existing_branch_projects(projects, branch, is_remote=True):
                cprint(' - No remote branches to prune\n', 'red')
                sys.exit()

            for project in projects:
                self._run_project_command(project, skip, 'prune', branch, remote=True)

    def _reset_parallel(self, group_names, project_names=None, skip=None, timestamp_project=None):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel"""

        if skip is None:
            skip = []

        print(' - Reset projects in parallel\n')
        timestamp = None
        if timestamp_project:
            timestamp = self._get_timestamp(timestamp_project)

        if project_names is None:
            groups = [g for g in self.groups if g.name in group_names]
            self._validate_groups(groups)
            projects = [p for g in self.groups if g.name in group_names for p in g.projects]
            self._print_parallel_groups_output(groups, skip)
            for project in projects:
                if project.name in skip:
                    continue
                result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
                __clowder_results__.append(result)
            pool_handler(len(projects))
            return

        projects = [p for g in self.groups for p in g.projects if p.name in project_names]
        self._validate_projects(projects)
        self._print_parallel_projects_output(projects, skip)
        for project in projects:
            if project.name in skip:
                continue
            result = __clowder_pool__.apply_async(reset_project, args=(project, timestamp), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    @staticmethod
    def _run_group_command(group, skip, command, *args, **kwargs):
        """Run group command and print output"""

        print(fmt.group_name(group.name))
        for project in group.projects:
            print(project.status())
            if project.name in skip:
                print(fmt.skip_project_message())
                continue
            getattr(project, command)(*args, **kwargs)

    @staticmethod
    def _run_project_command(project, skip, command, *args, **kwargs):
        """Run project command and print output"""

        print(project.status())
        if project.name in skip:
            print(fmt.skip_project_message())
            return
        getattr(project, command)(*args, **kwargs)

    @staticmethod
    def _sync_parallel(projects, rebase=False):
        """Sync projects in parallel"""

        print(' - Sync forks in parallel\n')
        for project in projects:
            print(project.status())
            if project.fork:
                print('  ' + fmt.fork_string(project.name))
                print('  ' + fmt.fork_string(project.fork.name))

        for project in projects:
            result = __clowder_pool__.apply_async(sync_project, args=(project, rebase), callback=async_callback)
            __clowder_results__.append(result)
        pool_handler(len(projects))

    @staticmethod
    def _validate_groups(groups):
        """Validate status of all projects for specified groups"""

        for group in groups:
            group.print_validation()

        if not all([g.is_valid() for g in groups]):
            print()
            sys.exit(1)

    @staticmethod
    def _validate_projects(projects):
        """Validate status of all projects"""

        if not all([p.is_valid() for p in projects]):
            print()
            sys.exit(1)

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups"""

        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.existing_projects():
                projects_exist = False

        if not projects_exist:
            herd_output = fmt.clowder_command('clowder herd')
            print('\n - First run ' + herd_output + ' to clone missing projects\n')
            sys.exit(1)

    def _validate_yaml(self, yaml_file, max_import_depth):
        """Validate clowder.yaml"""

        parsed_yaml = clowder_yaml.parse_yaml(yaml_file)
        if max_import_depth < 0:
            print(fmt.invalid_yaml_error())
            print(fmt.recursive_import_error(self._max_import_depth))
            print()
            sys.exit(1)

        if 'import' not in parsed_yaml:
            clowder_yaml.validate_yaml(yaml_file)
            return

        clowder_yaml.validate_yaml_import(yaml_file)
        imported_clowder = parsed_yaml['import']

        try:
            if imported_clowder == 'default':
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'clowder.yaml')
            else:
                imported_yaml_file = os.path.join(self.root_directory, '.clowder', 'versions',
                                                  imported_clowder, 'clowder.yaml')
            if not os.path.isfile(imported_yaml_file):
                error = fmt.missing_imported_yaml_error(imported_yaml_file, yaml_file)
                raise ClowderError(error)
            yaml_file = imported_yaml_file
            self._validate_yaml(yaml_file, max_import_depth - 1)
        except ClowderError as err:
            print(fmt.invalid_yaml_error())
            print(fmt.error(err))
            sys.exit(1)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)


# Disable warnings shown by pylint for catching too general exception
# pylint: disable=W0703


def pool_handler(count):
    """Pool handler for finishing parallel jobs"""

    print()
    __clowder_progress__.start(count)

    try:
        for result in __clowder_results__:
            result.get()
            if not result.successful():
                __clowder_progress__.close()
                __clowder_pool__.close()
                __clowder_pool__.terminate()
                cprint('\n - Command failed\n', 'red')
                sys.exit(1)
    except Exception as err:
        __clowder_progress__.close()
        __clowder_pool__.close()
        __clowder_pool__.terminate()
        cprint('\n' + str(err) + '\n', 'red')
        sys.exit(1)
    else:
        __clowder_progress__.complete()
        __clowder_progress__.close()
        __clowder_pool__.close()
        __clowder_pool__.join()
