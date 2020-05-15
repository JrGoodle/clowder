# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List

import clowder.util.formatting as fmt
from clowder import CLOWDER_YAML
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError, ClowderYAMLYErrorType
from clowder.model.defaults import Defaults
from clowder.model.project import Project
from clowder.model.source import Source
from clowder.util.clowder_utils import (
    filter_projects,
    print_parallel_projects_output,
    validate_projects
)
from clowder.util.yaml import load_yaml, validate_yaml


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar dict defaults: Global clowder.yaml defaults
    :ivar list[Group] groups: List of all Groups
    :ivar list[Source] sources: List of all Sources
    :ivar Optional[Exception] error: Exception from failing to load clowder.yaml
    """

    def __init__(self):
        """ClowderController __init__

        :raise ClowderExit:
        """

        self.defaults = None
        self.sources = []
        self.projects = []
        self.error = None
        self.project_names = []

        try:
            if CLOWDER_YAML is None:
                raise ClowderYAMLError(fmt.error_missing_yaml(), ClowderYAMLYErrorType.MISSING_YAML)
            validate_yaml()
            self._load_yaml()
        except ClowderYAMLError as err:
            self.error = err
        except (KeyboardInterrupt, SystemExit):
            raise ClowderExit(1)

    def get_all_fork_project_names(self) -> List[str]:
        """Returns all project names containing forks

        :return: List of project names containing forks
        :rtype: list[str]
        """

        try:
            return sorted([p.name for p in self.projects if p.fork is not None])
        except TypeError:
            return []

    def get_all_project_paths(self) -> List[str]:
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list[str]
        """

        try:
            return sorted([p.formatted_project_path() for p in self.projects])
        except TypeError:
            return []

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

        return {'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'projects': projects}

    def validate_print_output(self, project_names: List[str]) -> None:
        """Validate projects/groups and print output

        :param Optional[List[str]] project_names: Project names to validate/print
        """

        projects = filter_projects(self.projects, project_names)
        validate_projects(projects)
        print_parallel_projects_output(projects)

    def validate_projects_exist(self) -> None:
        """Validate existence status of all projects for specified groups

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

    def _get_all_project_names(self) -> List[str]:
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list[str]
        """

        try:
            names = [g for p in self.projects for g in p.groups]
            return sorted(list(set(names)))
        except TypeError:
            return []

    def _load_yaml(self) -> None:
        """Load clowder.yaml"""
        try:
            yaml = load_yaml()
            self.defaults = Defaults(yaml['defaults'])
            self.sources = [Source(s, self.defaults) for s in yaml['sources']]
            for project in yaml['projects']:
                self.projects.append(Project(project, self.defaults, self.sources))
            self.project_names = self._get_all_project_names()
        except (AttributeError, KeyError, TypeError):
            self.defaults = None
            self.sources = []
            self.projects = []


CLOWDER_CONTROLLER = ClowderController()
