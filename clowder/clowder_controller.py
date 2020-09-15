# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.data import ResolvedProject, SOURCE_CONTROLLER
from clowder.data.model import ClowderBase
from clowder.data.util import (
    print_parallel_projects_output,
    validate_project_statuses
)
from clowder.util.yaml import load_yaml_file, validate_yaml_file


class ClowderController(object):
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

        :raise ClowderError:
        """

        self.error: Optional[Exception] = None

        self._initialize_properties()

        try:
            if ENVIRONMENT.clowder_yaml is None:
                err = ClowderError(ClowderErrorType.YAML_MISSING_FILE, fmt.error_missing_clowder_yaml())
                LOG_DEBUG('Failed to initialize clowder controller', err)
                raise err
            yaml = load_yaml_file(ENVIRONMENT.clowder_yaml, ENVIRONMENT.clowder_dir)
            validate_yaml_file(yaml, ENVIRONMENT.clowder_yaml)

            self._clowder = ClowderBase(yaml)

            # Register all sources as we come across them
            defaults = self._clowder.defaults
            if defaults is not None and defaults.source is not None:
                SOURCE_CONTROLLER.add_source(defaults.source)

            sources = self._clowder.sources
            if sources is not None:
                for s in sources:
                    SOURCE_CONTROLLER.add_source(s)

            # Load from array
            projects = self._clowder.clowder.projects
            if projects is not None:
                for project in projects:
                    SOURCE_CONTROLLER.add_source(project.source)
                    if project.upstream is not None:
                        SOURCE_CONTROLLER.add_source(project.upstream.source)
                # Validate all source names have a defined source with url
                SOURCE_CONTROLLER.validate_sources()

                resolved_projects = [ResolvedProject(p, defaults=defaults, protocol=self._clowder.protocol)
                                     for p in projects]
                self.projects = tuple(sorted(resolved_projects, key=lambda p: p.name))
                self._update_properties()
                return

            # Load from dict
            groups = self._clowder.clowder.groups
            projects = [p for g in groups for p in g.projects]
            for project in projects:
                SOURCE_CONTROLLER.add_source(project.source)
                upstream = project.upstream
                if upstream is not None:
                    SOURCE_CONTROLLER.add_source(upstream.source)
            # Validate all source names have a defined source with url
            SOURCE_CONTROLLER.validate_sources()

            resolved_projects = [ResolvedProject(p, defaults=defaults, group=g, protocol=self._clowder.protocol)
                                 for g in groups for p in g.projects]
            self.projects = tuple(sorted(resolved_projects, key=lambda p: p.name))
            self._update_properties()
        except ClowderError as err:
            LOG_DEBUG('Failed to init clowder controller', err)
            self.error = err
            self._initialize_properties()
        except (AttributeError, KeyError, TypeError) as err:
            LOG_DEBUG('Failed to load clowder yaml', err)
            self.error = err
            self._initialize_properties()

    def get_all_upstream_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing upstreams

        :return: All project names containing upstreams
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.name for p in self.projects if p.upstream is not None]))
        except TypeError as err:
            LOG_DEBUG('Failed to get upstream project names', err)
            return ()

    @staticmethod
    def get_projects_output(projects: Tuple[ResolvedProject, ...]) -> Tuple[str, ...]:
        """Returns all project paths/names output for specified projects

        :param Tuple[ResolvedProject, ...] projects: Projects to get paths/names output of
        :return: All project paths
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.formatted_project_output() for p in projects]))
        except TypeError as err:
            LOG_DEBUG('Failed to get projects output', err)
            return ()

    def get_timestamp(self, timestamp_project: str) -> str:
        """Return timestamp for project

        :param str timestamp_project: Project to get timestamp of current HEAD commit
        :return: Commit timestamp string
        :rtype: str
        :raise ClowderError:
        """

        timestamp = None
        for project in self.projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            raise ClowderError(ClowderErrorType.GIT_ERROR, fmt.error_timestamp_not_found())

        return timestamp

    def get_project_sha(self, project_id: int, short: bool = False) -> str:
        """Return current project commit sha

        :return: Current active commit sha
        :rtype: str
        :raise ClowderError:
        """

        for project in self.projects:
            if project_id == id(project):
                return project.sha(short=short)

        err = ClowderError(ClowderErrorType.PROJECT_NOT_FOUND, fmt.error_project_not_found())
        LOG_DEBUG(f"Project with id {project_id} not found", err)
        raise err

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        return self._clowder.get_yaml(resolved=resolved)

    @staticmethod
    def validate_print_output(projects: Tuple[ResolvedProject, ...]) -> None:
        """Validate projects/groups and print output

        :param Tuple[ResolvedProject, ...] projects: Projects to validate/print
        """

        validate_project_statuses(projects)
        print_parallel_projects_output(projects)

    def validate_projects_exist(self) -> None:
        """Validate all projects exist on disk

        :raise ClowderError:
        """

        projects_exist = True
        for project in self.projects:
            project.print_existence_message()
            if not project.exists():
                projects_exist = False

        if not projects_exist:
            raise ClowderError(ClowderErrorType.INVALID_PROJECT_STATUS, fmt.error_clone_missing_projects())

    def _get_upstream_names(self) -> Tuple[str, ...]:
        """Returns all upstream names for current clowder yaml file

        :return: All upstream names
        :rtype: Tuple
        """

        try:
            upstream_names = [str(p.upstream.name) for p in self.projects if p.upstream is not None]
            return tuple(sorted(set(upstream_names)))
        except TypeError as err:
            LOG_DEBUG('Failed to get upstream names', err)
            return ()

    @staticmethod
    def _get_project_upstream_names(project_names, upstream_names) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project and upstream names
        :rtype: Tuple
        """

        return tuple(sorted(set(project_names + upstream_names)))

    def _get_project_names(self) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project names
        :rtype: Tuple
        """

        try:
            project_names = [str(p.name) for p in self.projects]
            return tuple(sorted(set(project_names)))
        except TypeError as err:
            LOG_DEBUG('Failed to get project names', err)
            return ()

    def _get_project_paths(self) -> Tuple[str, ...]:
        """Returns all project paths for current clowder yaml file

        :return: All project paths
        :rtype: Tuple
        """

        try:
            paths = [str(p.path) for p in self.projects]
            return tuple(sorted(set(paths)))
        except TypeError as err:
            LOG_DEBUG('Failed to get project paths', err)
            return ()

    def _get_project_groups(self, project_upstream_names, project_paths) -> Tuple[str, ...]:
        """Returns all project group names for current clowder yaml file

        :return: All project paths
        :rtype: Tuple
        """

        try:
            groups = [g for p in self.projects for g in p.groups]
            groups = [g for g in groups if g not in project_upstream_names and g not in project_paths]
            return tuple(sorted(set(groups)))
        except TypeError as err:
            LOG_DEBUG('Failed to get group names', err)
            return ()

    def _get_project_choices(self) -> Tuple[str, ...]:
        """Returns all project choices current clowder yaml file

        :return: All project paths
        :rtype: Tuple
        """

        try:
            names = [g for p in self.projects for g in p.groups]
            return tuple(sorted(set(names)))
        except TypeError as err:
            LOG_DEBUG('Failed to get project choices', err)
            return ()

    def _get_project_choices_with_default(self) -> Tuple[str, ...]:
        """Returns all project choices current clowder yaml file

        :return: All project paths
        :rtype: Tuple
        """

        try:
            names = [g for p in self.projects for g in p.groups]
            names.append('default')
            return tuple(sorted(set(names)))
        except TypeError as err:
            LOG_DEBUG('Failed to get project choices with default', err)
            return ()

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
        """Validate projects don't share share directories"""

        paths = [str(p.path.resolve()) for p in self.projects]
        duplicate = fmt.check_for_duplicates(paths)
        if duplicate is not None:
            self._initialize_properties()
            message = fmt.error_duplicate_project_path(duplicate, ENVIRONMENT.clowder_yaml)
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_PATH, message)

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


CLOWDER_CONTROLLER: ClowderController = ClowderController()
