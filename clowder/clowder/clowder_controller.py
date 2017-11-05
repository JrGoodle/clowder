# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

from termcolor import cprint

from clowder.error.clowder_yaml_error import ClowderYAMLError
from clowder.model.group import Group
from clowder.model.source import Source
from clowder.yaml.loading import load_yaml


class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder

    :ivar str root_directory: Root directory of clowder projects
    :ivar dict defaults: Global clowder.yaml defaults
    :ivar list[Group] groups: List of all Groups
    :ivar list[Source] sources: List of all Sources
    """

    def __init__(self, root_directory):
        """ClowderController __init__

        :param str root_directory: Root directory of clowder projects
        """

        self.root_directory = root_directory
        self.defaults = None
        self.groups = []
        self.sources = []
        self._max_import_depth = 10
        self.error = None
        try:
            self._load_yaml()
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except (ClowderYAMLError, KeyError) as err:
            self.error = err

    def get_all_fork_project_names(self):
        """Returns all project names containing forks

        :return: List of project names containing forks
        :rtype: list[str]
        """

        return sorted([p.name for g in self.groups for p in g.projects if p.fork])

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml

        :return: List of all group names
        :rtype: list[str]
        """

        return sorted([g.name for g in self.groups])

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml

        :return: List of all project names
        :rtype: list[str]
        """

        return sorted([p.name for g in self.groups for p in g.projects])

    def get_all_project_paths(self):
        """Returns all project paths for current clowder.yaml

        :return: List of all project paths
        :rtype: list[str]
        """

        return sorted([p.formatted_project_path() for g in self.groups for p in g.projects])

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

        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def get_yaml_resolved(self):
        """Return python object representation for resolved yaml

        :return: YAML python object
        :rtype: dict
        """

        groups_yaml = [g.get_yaml_resolved() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        return {'defaults': self.defaults,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def _load_yaml(self):
        """Load clowder.yaml"""
        yaml = load_yaml(self.root_directory)

        self.defaults = yaml['defaults']
        if 'depth' not in self.defaults:
            self.defaults['depth'] = 0

        self.sources = [Source(s) for s in yaml['sources']]
        for group in yaml['groups']:
            self.groups.append(Group(self.root_directory, group, self.defaults, self.sources))
