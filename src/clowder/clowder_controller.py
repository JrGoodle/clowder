# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Tuple

import clowder.util.formatting as fmt
from clowder import CLOWDER_YAML
from clowder.error import (
    ClowderExit,
    ClowderYAMLError, ClowderYAMLErrorType
)
from clowder.model import Defaults
from clowder.model import Project
from clowder.model import Source
from clowder.util.clowder_utils import (
    print_parallel_projects_output,
    validate_project_statuses
)
from clowder.util.yaml import load_clowder_yaml, validate_clowder_yaml


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar Optional[str] name: Name of clowder
    :ivar Optional[Defaults] defaults: Global clowder.yaml defaults
    :ivar Tuple[Group, ...] groups: List of all Groups
    :ivar Tuple[Source, ...] sources: List of all Sources
    :ivar Tuple[str, ...] project_names: All possible project and group names
    :ivar Tuple[str, ...] project_choices: All possible project and group choices
    :ivar Tuple[str, ...] project_choices_with_default: All possible project and group choices, including 'default'
    :ivar Optional[Exception] error: Exception from failing to load clowder.yaml
    """

    def __init__(self):
        """ClowderController __init__

        :raise ClowderExit:
        """

        self.error = None

        self.name = None
        self.defaults = None
        self.sources = ()
        self.projects = ()
        self.project_names = ()
        self.project_choices = ()
        self.project_choices_with_default = ('default',)

        try:
            if CLOWDER_YAML is None:
                raise ClowderYAMLError(fmt.error_missing_clowder_yaml(), ClowderYAMLErrorType.MISSING_YAML)
            yaml = load_clowder_yaml()
            validate_clowder_yaml(yaml)
            self._load_clowder_yaml(yaml)
        except ClowderYAMLError as err:
            self.error = err
        except (KeyboardInterrupt, SystemExit):
            raise ClowderExit(1)

    def get_all_fork_project_names(self) -> Tuple[str, ...]:
        """Returns all project names containing forks

        :return: All project names containing forks
        :rtype: Tuple[str, ...]
        """

        try:
            return tuple(sorted([p.name for p in self.projects if p.fork is not None]))
        except TypeError:
            return ()

    def get_project_paths(self, projects: Tuple[Project, ...]) -> Tuple[str, ...]: # noqa
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
        :raise ClowderExit:
        """

        timestamp = None
        for project in self.projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            print(fmt.error_timestamp_not_found())
            raise ClowderExit(1)

        return timestamp

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            projects = [p.get_yaml(resolved=True) for p in self.projects]
        else:
            projects = [p.get_yaml() for p in self.projects]

        return {'name': self.name,
                'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'projects': projects}

    def validate_print_output(self, projects: Tuple[Project, ...]) -> None: # noqa
        """Validate projects/groups and print output

        :param Tuple[Project, ...] projects: Projects to validate/print
        """

        validate_project_statuses(projects)
        print_parallel_projects_output(projects)

    def validate_projects_exist(self) -> None:
        """Validate all projects exist on disk

        :raise ClowderExit:
        """

        projects_exist = True
        for project in self.projects:
            project.print_existence_message()
            if not project.exists():
                projects_exist = False

        if not projects_exist:
            print(f"\n - First run {fmt.clowder_command('clowder herd')} to clone missing projects\n")
            raise ClowderExit(1)

    def _get_all_project_names(self) -> Tuple[str, ...]:
        """Returns all project names for current clowder.yaml

        :return: All project and group names
        :rtype: Tuple
        """

        try:
            names = [g for p in self.projects for g in p.groups]
            return tuple(sorted(set(names)))
        except TypeError:
            return ()

    def _load_clowder_yaml(self, yaml: dict) -> None:
        """Load clowder.yaml

        :param dict yaml: Parsed yaml dict
        """
        try:
            self.name = yaml['name']
            self.defaults = Defaults(yaml['defaults'])
            self.sources = tuple(sorted([Source(s, self.defaults) for s in yaml['sources']],
                                        key=lambda source: source.name))
            self.projects = tuple(sorted([Project(p, self.defaults, self.sources) for p in yaml['projects']],
                                         key=lambda project: project.name))
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
            raise ClowderExit(1)


CLOWDER_CONTROLLER: ClowderController = ClowderController()
