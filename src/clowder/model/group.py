# -*- coding: utf-8 -*-
"""Representation of clowder yaml group

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Tuple

from .defaults import Defaults
from .project import Project
from .source import Source


class GroupImpl(object):
    """clowder yaml GroupImpl model class

    :ivar str name: Source name
    :ivar Optional[str] path: Group path prefix
    """

    def __init__(self, name: str, group: dict):
        """Source __init__

        :param str name: Group name
        :param dict group: Parsed YAML python object for group
        """

        self.name = name
        self.path = group.get('path', None)
        self._groups = group.get('groups', None)


class Group(GroupImpl):
    """clowder yaml Group model class

    :ivar Optional[str] projects: Group projects
    """

    def __init__(self, name: str, group: dict, defaults: Defaults, sources: Tuple[Source, ...]):
        """Source __init__

        :param str name: Group name
        :param dict group: Parsed YAML python object for group
        :param Defaults defaults: Defaults instance
        :param Tuple[Source, ...] sources: List of Source instances
        """

        super().__init__(name, group)

        self.groups = group.get('groups', []) + [self.name]

        self.projects = [Project(p, defaults, sources, path_prefix=self.path, groups=self.groups)
                         for p in group["projects"]]

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation for saving yaml

        :param bool resolved: Whether to return resolved yaml
        :return: YAML python object
        :rtype: dict
        """

        if resolved:
            projects_yaml = [p.get_yaml(resolved_sha=p.sha()) for p in self.projects]
        else:
            projects_yaml = [p.get_yaml() for p in self.projects]
        group = {'projects': projects_yaml}

        if self.path is not None:
            group['path'] = self.path

        if self._groups is not None:
            group['groups'] = self._groups

        return group
