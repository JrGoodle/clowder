"""Clowder command controller class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import pkg_resources
from functools import wraps
from pathlib import Path
from typing import Optional, Tuple

from pygoodle.console import CONSOLE
from pygoodle.tasks import Task, TaskPool
from pygoodle.yaml import load_yaml_file, validate_yaml_file, MissingYamlError

import clowder.util.formatting as fmt
from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.git.util import get_default_project_branch, get_default_upstream_branch
from clowder.data import ResolvedProject, SOURCE_CONTROLLER
from clowder.data.model import ClowderBase
from clowder.util.error import (
    ClowderGitError,
    DuplicatePathError,
    ProjectNotFoundError,
    ProjectStatusError
)


def print_clowder_name(func):
    """Print clowder name"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if CLOWDER_CONTROLLER.name is not None:
            CONSOLE.stdout(f'{fmt.clowder_name(CLOWDER_CONTROLLER.name)}\n')
        return func(*args, **kwargs)

    return wrapper


def valid_clowder_yaml_required(func):
    """If clowder yaml file is invalid, print invalid yaml message and exit

    :raise AmbiguousYamlError:
    :raise MissingSourceError:
    :raise Exception:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.ambiguous_yaml_error is not None:
            raise ENVIRONMENT.ambiguous_yaml_error
        if ENVIRONMENT.missing_source_error is not None:
            raise ENVIRONMENT.missing_source_error
        if CLOWDER_CONTROLLER.error is not None:
            raise CLOWDER_CONTROLLER.error
        return func(*args, **kwargs)

    return wrapper


class ClowderController:
    """Class encapsulating project information from clowder yaml for controlling clowder

    :ivar str Optional[name]: Clowder name
    :ivar Tuple[ResolvedProject, ...] projects: List of all ResolvedProjects
    :ivar Tuple[str, ...] project_names: All possible project names
    :ivar Tuple[str, ...] upstream_names: All possible upstream names
    :ivar Tuple[str, ...] project_upstream_names: All possible project and upstream names
    :ivar Tuple[str, ...] project_paths: All possible project paths
    :ivar Tuple[str, ...] project_groups: All possible project groups
    :ivar Tuple[str, ...] project_choices: All possible project and group choices
    :ivar Tuple[str, ...] project_choices_with_default: All possible project and group choices, including 'default'
    :ivar Optional[Exception] error: Exception from failing to load clowder yaml file
    """

    def __init__(self):
        """ClowderController __init__

        :raise MissingYamlError:
        """

        self.error: Optional[Exception] = None

        self._initialize_properties()

        try:
            if ENVIRONMENT.clowder_yaml is None:
                raise MissingYamlError(f"{Path('clowder.yml')} appears to be missing")
            yaml = load_yaml_file(ENVIRONMENT.clowder_yaml, ENVIRONMENT.clowder_dir)
            clowder_schema = pkg_resources.resource_string(__name__, f"{ENVIRONMENT.clowder_yaml.stem}.schema.json")
            validate_yaml_file(yaml, clowder_schema)

            self._clowder = ClowderBase(yaml)

            # Register all sources as we come across them
            defaults = self._clowder.defaults
            if defaults is not None and defaults.source is not None:
                SOURCE_CONTROLLER.add_source(defaults.source)

            sources = self._clowder.sources
            if sources is not None:
                for s in sources:
                    SOURCE_CONTROLLER.add_source(s)

            projects = self._clowder.clowder.projects
            sections = self._clowder.clowder.sections
            if projects is None:
                projects = [p for s in sections for p in s.projects]

            for project in projects:
                SOURCE_CONTROLLER.add_source(project.source)
                if project.upstream is not None:
                    SOURCE_CONTROLLER.add_source(project.upstream.source)
            # Validate all source names have a defined source with url
            SOURCE_CONTROLLER.validate_sources()

            if sections is None:
                resolved_projects = [ResolvedProject(p, defaults=defaults, protocol=self._clowder.protocol)
                                     for p in projects]
            else:
                resolved_projects = [ResolvedProject(p, defaults=defaults, section=s, protocol=self._clowder.protocol)
                                     for s in sections for p in s.projects]

            self.projects = tuple(sorted(resolved_projects, key=lambda p: p.name))
            self._update_properties()
            self._populate_default_branches()
        except Exception as err:
            LOG.debug('Failed to init clowder controller')
            self.error = err
            self._initialize_properties()

    @staticmethod
    def filter_projects(projects: Tuple[ResolvedProject, ...],
                        project_names: Tuple[str, ...]) -> Tuple[ResolvedProject, ...]:
        """Filter projects based on given project or group names

        :param Tuple[ResolvedProject, ...] projects: Projects to filter
        :param Tuple[str, ...] project_names: Project names to match against
        :return: Projects in groups matching given names
        """

        filtered_projects = []
        for name in project_names:
            filtered_projects += [p for p in projects if name in p.groups]
        return tuple(sorted(set(filtered_projects), key=lambda project: project.name))

    def get_all_upstream_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing upstreams

        :return: All project names containing upstreams
        """

        return tuple(sorted([p.name for p in self.projects if p.upstream is not None]))

    @staticmethod
    def get_projects_output(projects: Tuple[ResolvedProject, ...]) -> Tuple[str, ...]:
        """Returns all project paths/names output for specified projects

        :param Tuple[ResolvedProject, ...] projects: Projects to get paths/names output of
        :return: All project paths
        """

        return tuple(sorted([p.formatted_project_output() for p in projects]))

    def get_timestamp(self, timestamp_project: str) -> str:
        """Return timestamp for project

        :param str timestamp_project: Project to get timestamp of current HEAD commit
        :return: Commit timestamp string
        :raise ClowderGitError:
        """

        timestamp = None
        for project in self.projects:
            if project.name == timestamp_project:
                timestamp = project.current_timestamp

        if timestamp is None:
            raise ClowderGitError("Failed to find timestamp")

        return timestamp

    def get_project_sha(self, project_id: int, short: bool = False) -> str:
        """Return current project commit sha

        :return: Current active commit sha
        :raise ProjectNotFoundError:
        """

        for project in self.projects:
            if project_id == id(project):
                return project.sha(short=short)

        raise ProjectNotFoundError(f"Project with id {project_id} not found")

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        """

        return self._clowder.get_yaml(resolved=resolved)

    @staticmethod
    def project_has_branch(projects: Tuple[ResolvedProject, ...], branch: str, is_remote: bool) -> bool:
        """Checks if given branch exists in any project

        :param Tuple[ResolvedProject, ...] projects: Projects to check
        :param str branch: Branch to check for
        :param bool is_remote: Check for remote branch
        :return: True, if at least one branch exists
        """

        return any([p.has_branch(branch, is_remote=is_remote) for p in projects])

    @staticmethod
    def validate_project_statuses(projects: Tuple[ResolvedProject, ...], allow_missing_repo: bool = True) -> None:
        """Validate status of all projects

        :param Tuple[ResolvedProject, ...] projects: Projects to validate
        :param bool allow_missing_repo: Whether to allow validation to succeed with missing repo
        :raise ProjectStatusError:
        """

        for p in projects:
            p.print_validation(allow_missing_repo=allow_missing_repo)
        if not all([p.is_valid(allow_missing_repo=allow_missing_repo) for p in projects]):
            CONSOLE.stdout()
            raise ProjectStatusError("Invalid project state")

    @staticmethod
    def validate_print_output(projects: Tuple[ResolvedProject, ...]) -> None:
        """Validate projects/groups and print output

        :param Tuple[ResolvedProject, ...] projects: Projects to validate/print
        """

        CLOWDER_CONTROLLER.validate_project_statuses(projects)

    def validate_projects_exist(self) -> None:
        """Validate all projects exist on disk

        :raise ProjectStatusError:
        """

        projects_exist = True
        for project in self.projects:
            project.print_existence_message()
            if not project.exists():
                projects_exist = False

        if not projects_exist:
            raise ProjectStatusError(f"First run {fmt.clowder_command('clowder herd')} to clone missing projects")

    def _get_upstream_names(self) -> Tuple[str, ...]:
        """Returns all upstream names for current clowder yaml file

        :return: All upstream names
        """

        upstream_names = [str(p.upstream.name) for p in self.projects if p.upstream is not None]
        return tuple(sorted(set(upstream_names)))

    @staticmethod
    def _get_project_upstream_names(project_names, upstream_names) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project and upstream names
        """

        return tuple(sorted(set(project_names + upstream_names)))

    def _get_project_names(self) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project names
        """

        project_names = [str(p.name) for p in self.projects]
        return tuple(sorted(set(project_names)))

    def _get_project_paths(self) -> Tuple[str, ...]:
        """Returns all project paths for current clowder yaml file

        :return: All project paths
        """

        paths = [str(p.path) for p in self.projects]
        return tuple(sorted(set(paths)))

    def _get_project_groups(self, project_upstream_names, project_paths) -> Tuple[str, ...]:
        """Returns all project group names for current clowder yaml file

        :return: All project paths
        """

        groups = [g for p in self.projects for g in p.groups]
        groups = [g for g in groups if g not in project_upstream_names and g not in project_paths]
        return tuple(sorted(set(groups)))

    def _get_project_choices(self) -> Tuple[str, ...]:
        """Returns all project choices current clowder yaml file

        :return: All project paths
        """

        names = [g for p in self.projects for g in p.groups]
        return tuple(sorted(set(names)))

    def _get_project_choices_with_default(self) -> Tuple[str, ...]:
        """Returns all project choices current clowder yaml file

        :return: All project paths
        """

        names = [g for p in self.projects for g in p.groups]
        names.append('default')
        return tuple(sorted(set(names)))

    def _initialize_properties(self) -> None:
        """Initialize all properties"""

        self.name: Optional[str] = None
        self.projects: Tuple[ResolvedProject, ...] = ()
        self.project_names: Tuple[str, ...] = ()
        self.upstream_names: Tuple[str, ...] = ()
        self.project_upstream_names: Tuple[str, ...] = ()
        self.project_paths: Tuple[str, ...] = ()
        self.project_groups: Tuple[str, ...] = ()
        self.project_choices: Tuple[str, ...] = ()
        self.project_choices_with_default: Tuple[str, ...] = ('default',)

    def _validate_project_paths(self) -> None:
        """Validate projects don't share share directories

        :raise DuplicatePathError:
        """

        paths = [str(p.path.resolve()) for p in self.projects]
        duplicate = fmt.check_for_duplicates(paths)
        if duplicate is not None:
            self._initialize_properties()
            message = f"{fmt.invalid_yaml(ENVIRONMENT.clowder_yaml.name)}\n" \
                      f"{fmt.path(ENVIRONMENT.clowder_yaml)}\n" \
                      f"Multiple projects with path '{duplicate}'"
            raise DuplicatePathError(message)

    def _update_properties(self) -> None:
        """Initialize all properties"""

        self.name: Optional[str] = self._clowder.name

        self.project_names: Tuple[str, ...] = self._get_project_names()
        self.upstream_names: Tuple[str, ...] = self._get_upstream_names()
        self.project_upstream_names: Tuple[str, ...] = self._get_project_upstream_names(self.project_names,
                                                                                        self.upstream_names)
        self.project_paths: Tuple[str, ...] = self._get_project_paths()
        self.project_groups: Tuple[str, ...] = self._get_project_groups(self.project_upstream_names,
                                                                        self.project_paths)
        self.project_choices: Tuple[str, ...] = self._get_project_choices()
        self.project_choices_with_default: Tuple[str, ...] = self._get_project_choices_with_default()

        # Now that all the data is loaded, check that no projects share paths
        self._validate_project_paths()

    def _populate_default_branches(self) -> None:
        """Get default branch"""

        class DefaultBranchTask(Task):
            def __init__(self, project: ResolvedProject):
                self._project: ResolvedProject = project
                super().__init__(str(self._project.path))

            def run(self) -> None:
                if self._project.ref is None:
                    default_branch = get_default_project_branch(self._project.full_path,
                                                                self._project.remote,
                                                                self._project.url)
                    self._project.update_default_branch(default_branch)
                if self._project.upstream is not None and self._project.upstream.ref is None:
                    upstream = self._project.upstream
                    default_branch = get_default_upstream_branch(upstream.full_path,
                                                                 upstream.remote,
                                                                 upstream.url)
                    upstream.update_default_branch(default_branch)

        pool = TaskPool(jobs=5)
        tasks = [DefaultBranchTask(project) for project in self.projects]
        pool.run(tasks)


CLOWDER_CONTROLLER: ClowderController = ClowderController()
