# -*- coding: utf-8 -*-
"""Representation of clowder yaml group

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union
from clowder.error import ClowderError, ClowderErrorType
from .defaults import Defaults
from .project import Project
from .source import Source


class Group:
    """clowder yaml Group model class

    :ivar str name: Group name
    :ivar Optional[str] path: Group path prefix
    :ivar Optional[List[Group]] groups: Group names
    :ivar Optional[Defaults] defaults: Group defaults
    :ivar List[Project] projects: Group projects
    :ivar bool _has_projects_key: Whether the projects were listed under the 'projects' key in the yaml
    """

    def __init__(self, name: str, yaml: Union[dict, List[Project]]):
        """Group __init__

        :param str name: Group name
        :param Union[dict, List[Project]] yaml: Parsed YAML python object for group
        """

        self.name: str = name

        if isinstance(yaml, dict):
            self.path: Optional[str] = yaml.get('path', None)
            self.groups: Optional[List[Group]] = yaml.get('groups', None)
            self.projects = [Project(p) for p in yaml["projects"]]
        elif isinstance(yaml, list):
            self.path = None
            self.groups = None
            self.projects: List[Project] = [Project(p) for p in yaml]
        else:
            # TODO: Create new error type
            raise ClowderError(ClowderErrorType.YAML_UNKNOWN, "Wrong instance type for group")

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
