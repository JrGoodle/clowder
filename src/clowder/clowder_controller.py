# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.error.clowder_exit import ClowderExit
from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.model.defaults import Defaults
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.util.clowder_utils import (
    filter_groups,
    filter_projects,
    print_parallel_groups_output,
    print_parallel_projects_output,
    validate_groups,
    validate_projects
)
from clowder.yaml.loading import load_yaml


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar dict defaults: Global clowder.yaml defaults
    :ivar list[Group] groups: List of all Groups
    :ivar list[Source] sources: List of all Sources
    """

    def __init__(self):
        """ClowderController __init__

        :raise ClowderExit:
        """

        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10
        self.error = None
        try:
            self._load_yaml()
        except (ClowderYAMLError, KeyError) as err:
            self.error = err
        except (KeyboardInterrupt, SystemExit):
            raise ClowderExit(1)

    def get_all_fork_project_names(self) -> List[str]:
        """Returns all project names containing forks

        :return: List of project names containing forks
        :rtype: list[str]
        """

        try:
            return sorted([p.name for g in self.groups for p in g.projects if p.fork])
        except TypeError:
            return []

    def get_all_group_names(self) -> List[str]:
        """Returns all group names for current clowder.yaml

        :return: List of all group names
        :rtype: list[str]
        """

        try:
            return sorted([g.name for g in self.groups])
        except TypeError:
            return []

    def get_all_project_names(self) -> List[str]:
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list[str]
        """

        try:
            return sorted([p.name for g in self.groups for p in g.projects])
        except TypeError:
            return []

    def get_all_project_paths(self) -> List[str]:
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list[str]
        """

        try:
            return sorted([p.formatted_project_path() for g in self.groups for p in g.projects])
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
        all_projects = [p for g in self.groups for p in g.projects]
        for project in all_projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            cprint(' - Failed to find timestamp\n', 'red')
            raise ClowderExit(1)

        return timestamp

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation of model objects

        .. py:function:: get_yaml(self, resolved=False)

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            groups = [g.get_yaml(resolved=True) for g in self.groups]
        else:
            groups = [g.get_yaml() for g in self.groups]

        return {'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'groups': groups}

    def validate_print_output(self, group_names: List[str], project_names: Optional[List[str]] = None,
                              skip: Optional[List[str]] = None) -> None:
        """Validate projects/groups and print output

        .. py:function:: validate_print_output(group_names, project_names=None, skip=[])

        :param list[str] group_names: Group names to validate/print
        :param Optional[List[str]] project_names: Project names to validate/print
        :param Optional[List[str]] skip: Project names to skip
        """

        skip = [] if skip is None else skip

        if project_names is None:
            groups = filter_groups(self.groups, group_names)
            validate_groups(groups)
            print_parallel_groups_output(groups, skip)
            return

        projects = filter_projects(self.groups, project_names=project_names)
        validate_projects(projects)
        print_parallel_projects_output(projects, skip)

    def validate_projects_exist(self) -> None:
        """Validate existence status of all projects for specified groups

        :raise ClowderExit:
        """

        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.existing_projects():
                projects_exist = False

        if not projects_exist:
            herd_output = fmt.clowder_command('clowder herd')
            print('\n - First run ' + herd_output + ' to clone missing projects\n')
            raise ClowderExit(1)

    def _load_yaml(self) -> None:
        """Load clowder.yaml"""
        try:
            yaml = load_yaml()
            self.defaults = Defaults(yaml['defaults'])
            self.sources = [Source(s, self.defaults) for s in yaml['sources']]
            for group in yaml['groups']:
                self.groups.append(Group(group, self.defaults, self.sources))
        except (AttributeError, TypeError):
            self.defaults = None
            self.sources = []
            self.groups = []


CLOWDER_CONTROLLER = ClowderController()
