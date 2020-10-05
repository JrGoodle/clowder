# -*- coding: utf-8 -*-
"""Representation of clowder yaml group

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union
from pathlib import Path

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

from .defaults import Defaults
from .project import Project


class Group:
    """clowder yaml Group model class

    :ivar str name: Group name
    :ivar Optional[Path] path: Group path prefix
    :ivar Optional[List[Group]] groups: Group names
    :ivar Optional[Defaults] defaults: Group defaults
    :ivar List[Project] projects: Group projects
    :ivar Optional[str] protocol: Git protocol
    :ivar bool _has_projects_key: Whether the projects were listed under the 'projects' key in the yaml file
    """

    def __init__(self, name: str, yaml: Union[dict, List[Project]]):
        """Group __init__

        :param str name: Group name
        :param Union[dict, List[Project]] yaml: Parsed YAML python object for group
        """

        self.name: str = name

        if isinstance(yaml, dict):
            path = yaml.get('path', None)
            self.path: Optional[Path] = Path(path) if path is not None else None
            self.groups: Optional[List[Group]] = yaml.get('groups', None)
            defaults = yaml.get("defaults", None)
            self.defaults: Optional[Defaults] = Defaults(defaults) if defaults is not None else None
            self.protocol: Optional[str] = yaml.get('protocol', None)
            self.projects: List[Project] = [Project(p) for p in yaml["projects"]]
            self._has_projects_key: bool = True
        elif isinstance(yaml, list):
            self.path: Optional[Path] = None
            self.groups: Optional[List[Group]] = None
            self.defaults: Optional[Defaults] = None
            self.protocol: Optional[str] = None
            self.projects: List[Project] = [Project(p) for p in yaml]
            self._has_projects_key: bool = False
        else:
            err = ClowderError(ClowderErrorType.WRONG_GROUP_TYPE, fmt.error_wrong_group_type())
            LOG_DEBUG("Wrong instance type for group", err)
            raise err

    def get_yaml(self, resolved: bool = False) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[dict, list]
        """

        if not self._has_projects_key:
            return [p.get_yaml(resolved=resolved) for p in self.projects]

        yaml = {}

        if self.path is not None:
            yaml['path'] = str(self.path)
        if self.protocol is not None:
            yaml['protocol'] = self.protocol
        if self.groups is not None:
            yaml['groups'] = str(self.groups)
        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()

        yaml["projects"] = [p.get_yaml(resolved=resolved) for p in self.projects]

        return yaml
