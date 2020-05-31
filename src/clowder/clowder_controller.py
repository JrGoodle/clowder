# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
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
    :ivar Tuple[str, ...] project_names: All possible project and group names
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
        self.project_choices: Tuple[str, ...] = ()
        self.project_choices_with_default = ('default',)

        try:
            if ENVIRONMENT.clowder_yaml is None:
                raise ClowderError(ClowderErrorType.YAML_MISSING_FILE, fmt.error_missing_clowder_yaml())
            yaml = load_yaml_file(ENVIRONMENT.clowder_yaml, ENVIRONMENT.clowder_dir)
            validate_yaml_file(yaml, ENVIRONMENT.clowder_yaml)
            self._load_clowder_yaml(yaml)
        except ClowderError as err:
            self.error = err
        except (KeyboardInterrupt, SystemExit):
            raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())

    def get_all_fork_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing forks

        :return: All project names containing forks
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.name for p in self.projects if p.fork is not None]))
        except TypeError:
            return ()

    @staticmethod
    def get_project_paths(projects: Tuple[Project, ...]) -> Tuple[str, ...]:
        """Returns all project paths for specified projects

        :param Tuple[Project, ...] projects: Projects to get paths of
        :return: All project paths
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.formatted_project_path() for p in projects]))
        except TypeError:
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

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            projects = [p.get_yaml(resolved_sha=p.sha()) for p in self.projects]
        else:
            projects = [p.get_yaml() for p in self.projects]

        return {'name': self.name,
                'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'projects': projects}

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

    def _get_all_project_names(self) -> Tuple[str, ...]:
        """Returns all project names for current clowder yaml file

        :return: All project and group names
        :rtype: Tuple
        """

        try:
            names = [g for p in self.projects for g in p.groups]
            return tuple(sorted(set(names)))
        except TypeError:
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

            self.project_names = self._get_all_project_names()
            names = list(self.project_names)
            self.project_choices = tuple(sorted(set(names)))
            names.append('default')
            self.project_choices_with_default = tuple(sorted(set(names)))
        except (AttributeError, KeyError, TypeError) as err:
            self.name = None
            self.defaults = None
            self.sources = ()
            self.projects = ()
            self.project_names = ()
            self.project_choices = ()
            self.project_choices_with_default = ('default',)
            self.error = err
        except (KeyboardInterrupt, SystemExit):
            raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())


CLOWDER_CONTROLLER: ClowderController = ClowderController()
