# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from termcolor import cprint

from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.model.defaults import Defaults
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.yaml.loading import load_yaml


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar dict defaults: Global clowder.yaml defaults
    :ivar list[Group] groups: List of all Groups
    :ivar list[Source] sources: List of all Sources
    """

    def __init__(self):
        """ClowderController __init__"""

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
            sys.exit(1)

    def get_all_fork_project_names(self):
        """Returns all project names containing forks

        :return: List of project names containing forks
        :rtype: list[str]
        """

        try:
            return sorted([p.name for g in self.groups for p in g.projects if p.fork])
        except TypeError:
            return []

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml

        :return: List of all group names
        :rtype: list[str]
        """

        try:
            return sorted([g.name for g in self.groups])
        except TypeError:
            return []

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list[str]
        """

        try:
            return sorted([p.name for g in self.groups for p in g.projects])
        except TypeError:
            return []

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list[str]
        """

        try:
            return sorted([p.formatted_project_path() for g in self.groups for p in g.projects])
        except TypeError:
            return []

    def get_timestamp(self, timestamp_project):
        """Return timestamp for project

        :param str timestamp_project: Project to get timestamp of current HEAD commit
        :return: Commit timestamp string
        :rtype: str
        """

        timestamp = None
        all_projects = [p for g in self.groups for p in g.projects]
        for project in all_projects:
            if project.name == timestamp_project:
                timestamp = project.get_current_timestamp()

        if timestamp is None:
            cprint(' - Failed to find timestamp\n', 'red')
            sys.exit(1)

        return timestamp

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'groups': [g.get_yaml() for g in self.groups]}

    def get_yaml_resolved(self):
        """Return python object representation for resolved yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'defaults': self.defaults.get_yaml(),
                'sources': [s.get_yaml() for s in self.sources],
                'groups': [g.get_yaml_resolved() for g in self.groups]}

    def _load_yaml(self):
        """Load clowder.yaml"""
        try:
            yaml = load_yaml()
            self.defaults = Defaults(yaml['defaults'])
            self.sources = [Source(s) for s in yaml['sources']]
            for group in yaml['groups']:
                self.groups.append(Group(group, self.defaults, self.sources))
        except (AttributeError, TypeError):
            self.defaults = None
            self.sources = []
            self.groups = []
