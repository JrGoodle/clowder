"""Clowder command controller class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import pkg_resources
from functools import wraps
from pathlib import Path
from typing import Iterable, Optional, Tuple

from pygoodle.console import CONSOLE
from pygoodle.format import Format
# from pygoodle.tasks import Task, TaskPool
from pygoodle.util import sorted_tuple
from pygoodle.yaml import load_yaml_file, validate_yaml_file, MissingYamlError

import clowder.util.formatting as fmt
from clowder.controller import ProjectRepo, SOURCE_CONTROLLER
from clowder.log import LOG
from clowder.model import ClowderBase
from clowder.environment import ENVIRONMENT
from clowder.util.error import (
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
    :ivar Tuple[ProjectRepo, ...] projects: List of all ProjectRepos
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
                resolved_projects = [ProjectRepo(p, defaults=defaults, protocol=self._clowder.protocol)
                                     for p in projects]
            else:
                resolved_projects = [ProjectRepo(p, defaults=defaults, section=s, protocol=self._clowder.protocol)
                                     for s in sections for p in s.projects]

            self.projects = sorted_tuple(resolved_projects)
            self._update_properties()
            self._populate_default_branches()
        except Exception as err:
            LOG.debug('Failed to init clowder controller')
            self.error = err
            self._initialize_properties()

    @staticmethod
    def filter_projects(projects: Iterable[ProjectRepo],
                        project_names: Iterable[str]) -> Tuple[ProjectRepo, ...]:
        """Filter projects based on given project or group names

        :param Iterable[ProjectRepo] projects: Projects to filter
        :param Iterable[str] project_names: Project names to match against
        :return: Projects in groups matching given names
        """

        filtered_projects = []
        for name in project_names:
            filtered_projects += [p for p in projects if name in p.groups]
        return sorted_tuple(filtered_projects, unique=True)

    def get_all_upstream_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing upstreams

        :return: All project names containing upstreams
        """

        return sorted_tuple([p.name for p in self.projects if p.upstream is not None])

    @staticmethod
    def get_projects_output(projects: Iterable[ProjectRepo]) -> Tuple[str, ...]:
        """Returns all project paths/names output for specified projects

        :param Iterable[ProjectRepo] projects: Projects to get paths/names output of
        :return: All project paths
        """

        return sorted_tuple([p.repo.formatted_name() for p in projects])

    def get_timestamp(self, timestamp_project: str) -> str:
        """Return timestamp for project

        :param str timestamp_project: Project to get timestamp of current HEAD commit
        :return: Commit timestamp string
        :raise ClowderGitError:
        """

        timestamp = None
        for project in self.projects:
            if project.name == timestamp_project:
                timestamp = project.repo.current_timestamp

        if timestamp is None:
            raise Exception("Failed to find timestamp")

        return timestamp

    def get_project_sha(self, project_id: int, short: bool = False) -> str:
        """Return current project commit sha

        :return: Current active commit sha
        :raise ProjectNotFoundError:
        """

        for project in self.projects:
            if project_id == id(project):
                return project.repo.current_commit(short=short).short_ref

        raise ProjectNotFoundError(f"Project with id {project_id} not found")

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        """

        return self._clowder.get_yaml(resolved=resolved)

    @staticmethod
    def project_has_local_branch(projects: Iterable[ProjectRepo], branch: str) -> bool:
        """Checks if given branch exists in any project

        :param Iterable[ProjectRepo] projects: Projects to check
        :param str branch: Branch to check for
        :return: True, if at least one branch exists
        """

        return any([p.repo.has_local_branch(branch) for p in projects])

    @staticmethod
    def project_has_remote_branch(projects: Iterable[ProjectRepo], branch: str) -> bool:
        """Checks if given branch exists in any project

        :param Iterable[ProjectRepo] projects: Projects to check
        :param str branch: Branch to check for
        :return: True, if at least one branch exists
        """

        return any([p.repo.has_remote_branch(branch, p.default_remote.name) for p in projects])

    @staticmethod
    def validate_projects_state(projects: Iterable[ProjectRepo], allow_missing: bool = True) -> None:
        """Validate state of all projects

        :param Iterable[ProjectRepo] projects: Projects to validate
        :param bool allow_missing: Whether to allow validation to succeed with missing repo
        :raise ProjectStatusError:
        """

        for p in projects:
            p.repo.print_validation(allow_missing=allow_missing)
        if not all([p.repo.is_valid(allow_missing=allow_missing) for p in projects]):
            CONSOLE.stdout()
            raise ProjectStatusError("Invalid project state")

    def validate_projects_exist(self) -> None:
        """Validate all projects exist on disk

        :raise ProjectStatusError:
        """

        projects_exist = True
        for project in self.projects:
            if not project.repo.exists:
                # TODO: Make sure this prints correct output
                CONSOLE.stdout(project.status())
                projects_exist = False

        if not projects_exist:
            raise ProjectStatusError(f"First run {Format.bold('clowder herd')} to clone missing projects")

    def _initialize_properties(self) -> None:
        """Initialize all properties"""

        self.name: Optional[str] = None
        self.projects: Tuple[ProjectRepo, ...] = ()
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

        paths = [str(p.relative_path.resolve()) for p in self.projects]
        duplicate = fmt.check_for_duplicates(paths)
        if duplicate is not None:
            self._initialize_properties()
            message = f"{Format.path(ENVIRONMENT.clowder_yaml.name)} appears to be invalid\n" \
                      f"{Format.path(ENVIRONMENT.clowder_yaml)}\n" \
                      f"Multiple projects with path '{duplicate}'"
            raise DuplicatePathError(message)

    def _update_properties(self) -> None:
        """Initialize all properties"""

        self.name: Optional[str] = self._clowder.name

        project_names = [str(p.name) for p in self.projects]
        self.project_names: Tuple[str, ...] = sorted_tuple(project_names, unique=True)

        upstream_names = [str(p.upstream.name) for p in self.projects if p.upstream is not None]
        self.upstream_names: Tuple[str, ...] = sorted_tuple(upstream_names, unique=True)

        self.project_upstream_names: Tuple[str, ...] = sorted_tuple(project_names + upstream_names, unique=True)

        paths = [str(p.relative_path) for p in self.projects]
        self.project_paths: Tuple[str, ...] = sorted_tuple(paths, unique=True)

        groups = [g for p in self.projects for g in p.groups]
        groups = [g for g in groups if g not in self.project_upstream_names and g not in self.project_paths]
        self.project_groups: Tuple[str, ...] = sorted_tuple(groups, unique=True)

        choices = [g for p in self.projects for g in p.groups]
        self.project_choices: Tuple[str, ...] = sorted_tuple(choices, unique=True)
        choices.append('default')
        self.project_choices_with_default: Tuple[str, ...] = sorted_tuple(choices, unique=True)

        # Now that all the data is loaded, check that no projects share paths
        self._validate_project_paths()

    def _populate_default_branches(self) -> None:
        """Get default branch"""

        raise NotImplementedError
        # class DefaultBranchTask(Task):
        #     def __init__(self, project: ProjectRepo):
        #         self._project: ProjectRepo = project
        #         super().__init__(str(self._project.path))
        #
        #     def run(self) -> None:
        #         if self._project.default_ref is None:
        #             default_branch = get_default_project_branch(self._project.full_path,
        #                                                         self._project.remote,
        #                                                         self._project.url)
        #             self._project.update_default_branch(default_branch)
        #         if self._project.upstream is not None and self._project.upstream.ref is None:
        #             upstream = self._project.upstream
        #             default_branch = get_default_upstream_branch(upstream.full_path,
        #                                                          upstream.remote,
        #                                                          upstream.url)
        #             upstream.update_default_branch(default_branch)
        #
        # pool = TaskPool(jobs=5)
        # tasks = [DefaultBranchTask(project) for project in self.projects]
        # pool.run(tasks)


CLOWDER_CONTROLLER: ClowderController = ClowderController()
