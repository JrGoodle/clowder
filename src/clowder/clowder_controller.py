# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.model import Defaults, Project, Source
from clowder.model.util import (
    print_parallel_projects_output,
    validate_project_statuses
)
from clowder.util.yaml import load_yaml_file, validate_yaml_file


class ClowderController(object):
    """Class encapsulating project information from clowder yaml for controlling clowder

    :ivar Optional[str] name: Name of clowder
    :ivar Optional[Defaults] defaults: Global clowder yaml defaults
    :ivar Tuple[Group, ...] groups: List of all Groups
    :ivar Tuple[Source, ...] sources: List of all Sources
    :ivar Tuple[str, ...] project_names: All possible project names
    :ivar Tuple[str, ...] fork_names: All possible fork names
    :ivar Tuple[str, ...] project_fork_names: All possible project and fork names
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

        self.name: Optional[str] = None
        self.defaults: Optional[Defaults] = None
        self.sources: Tuple[Source, ...] = ()
        self.projects: Tuple[Project, ...] = ()
        self.project_names: Tuple[str, ...] = ()
        self.fork_names: Tuple[str, ...] = ()
        self.project_fork_names: Tuple[str, ...] = ()
        self.project_paths: Tuple[str, ...] = ()
        self.project_groups: Tuple[str, ...] = ()
        self.project_choices: Tuple[str, ...] = ()
        self.project_choices_with_default: Tuple[str, ...] = ('default',)

        try:
            if ENVIRONMENT.clowder_yaml is None:
                raise ClowderError(ClowderErrorType.YAML_MISSING_FILE, fmt.error_missing_clowder_yaml())
            yaml = load_yaml_file(ENVIRONMENT.clowder_yaml, ENVIRONMENT.clowder_dir)
            validate_yaml_file(yaml, ENVIRONMENT.clowder_yaml)
            self._load_clowder_yaml(yaml)
        except ClowderError as err:
            LOG_DEBUG('Failed to init clowder controller', err)
            self.error = err

    def get_all_fork_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing forks

        :return: All project names containing forks
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.name for p in self.projects if p.fork is not None]))
        except TypeError as err:
            LOG_DEBUG('Failed to get fork project names', err)
            return ()

    @staticmethod
    def get_projects_output(projects: Tuple[Project, ...]) -> Tuple[str, ...]:
        """Returns all project paths/names output for specified projects

        :param Tuple[Project, ...] projects: Projects to get paths/names output of
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

    def get_yaml(self, resolved: bool = False, projects: Optional[Tuple[Project, ...]] = None) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :param Optional[Tuple[Project, ...]] projects: Projects to get yaml for
        :return: YAML python object
        :rtype: dict
        """

        if projects is None:
            projects = self.projects

        if resolved:
            projects_yaml = [p.get_yaml(resolved_sha=p.sha()) for p in projects]
        else:
            projects_yaml = [p.get_yaml() for p in projects]

        return {'name': self.name,
                'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'projects': projects_yaml}

    @staticmethod
    def validate_print_output(projects: Tuple[Project, ...]) -> None:
        """Validate projects/groups and print output

        :param Tuple[Project, ...] projects: Projects to validate/print
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

    def _get_all_fork_names(self) -> Tuple[str, ...]:
        """Returns all fork names for current clowder yaml file

        :return: All fork names
        :rtype: Tuple
        """

        try:
            fork_names = [str(p.fork.name) for p in self.projects if p.fork is not None]
            return tuple(sorted(set(fork_names)))
        except TypeError as err:
            LOG_DEBUG('Failed to get fork names', err)
            return ()

    @staticmethod
    def _get_all_project_fork_names(project_names, fork_names) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project and fork names
        :rtype: Tuple
        """

        return tuple(sorted(set(project_names + fork_names)))

    def _get_all_project_names(self) -> Tuple[str, ...]:
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

    def _get_all_project_paths(self) -> Tuple[str, ...]:
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

    def _get_all_project_groups(self, project_fork_names, project_paths) -> Tuple[str, ...]:
        """Returns all project paths for current clowder yaml file

        :return: All project paths
        :rtype: Tuple
        """

        try:
            groups = [g for p in self.projects for g in p.groups]
            groups = [g for g in groups if g not in project_fork_names and g not in project_paths]
            return tuple(sorted(set(groups)))
        except TypeError as err:
            LOG_DEBUG('Failed to get group names', err)
            return ()

    def _get_all_project_choices(self) -> Tuple[str, ...]:
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

    def _get_all_project_choices_with_default(self) -> Tuple[str, ...]:
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

    def _load_clowder_yaml(self, yaml: dict) -> None:
        """Load clowder yaml file

        :param dict yaml: Parsed yaml dict
        """
        try:
            self.name = yaml['name']
            self.defaults = Defaults(yaml['defaults'])
            self.sources = tuple(sorted([Source(s, self.defaults) for s in yaml['sources']],
                                        key=lambda source: source.name))

            if len(self.sources) == 1 and self.defaults.source is None:
                self.defaults.source = self.sources[0].name
            elif len(self.sources) > 1 and self.defaults.source is None:
                raise ClowderError(ClowderErrorType.MISSING_DEFAULT_SOURCE, fmt.error_missing_default_source())

            if not any([s.name == self.defaults.source for s in self.sources]):
                message = fmt.error_source_default_not_found(self.defaults.source, ENVIRONMENT.clowder_yaml)
                raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)

            self.projects = tuple(sorted([Project(p, self.defaults, self.sources) for p in yaml['projects']],
                                         key=lambda project: project.name))
            # Validate projects don't share share directories
            paths = [str(p.path.resolve()) for p in self.projects]
            duplicate = fmt.check_for_duplicates(paths)
            if duplicate is not None:
                message = fmt.error_duplicate_project_path(Path(duplicate), ENVIRONMENT.clowder_yaml)
                raise ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_PATH, message)

            self.project_names: Tuple[str, ...] = self._get_all_project_names()
            self.fork_names: Tuple[str, ...] = self._get_all_fork_names()
            self.project_fork_names: Tuple[str, ...] = self._get_all_project_fork_names(self.project_names,
                                                                                        self.fork_names)
            self.project_paths: Tuple[str, ...] = self._get_all_project_paths()
            self.project_groups: Tuple[str, ...] = self._get_all_project_groups(self.project_fork_names,
                                                                                self.project_paths)
            self.project_choices = self._get_all_project_choices()
            self.project_choices_with_default = self._get_all_project_choices_with_default()
        except (AttributeError, KeyError, TypeError) as err:
            LOG_DEBUG('Failed to load clowder yaml', err)
            self.name = None
            self.defaults = None
            self.sources = ()
            self.projects = ()
            self.project_names = ()
            self.fork_names = ()
            self.project_fork_names = ()
            self.project_choices = ()
            self.project_choices_with_default = ('default',)
            self.error = err


CLOWDER_CONTROLLER: ClowderController = ClowderController()
