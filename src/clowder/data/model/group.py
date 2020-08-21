# -*- coding: utf-8 -*-
"""Representation of clowder yaml group

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union
from pathlib import Path

from clowder.error import ClowderError, ClowderErrorType

from .defaults import Defaults
from .project import Project


class Group:
    """clowder yaml Group model class

    :ivar str name: Group name
    :ivar Optional[Path] path: Group path prefix
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
            path = yaml.get('path', None)
            self.path: Optional[Path] = Path(path) if path is not None else None
            self.groups: Optional[List[Group]] = yaml.get('groups', None)
            defaults = yaml.get("defaults", None)
            self.defaults: Optional[Defaults] = Defaults(defaults) if defaults is not None else None
            self.projects = [Project(p) for p in yaml["projects"]]
            self._has_projects_key = True
        elif isinstance(yaml, list):
            self.path = None
            self.groups = None
            self.defaults = None
            self.projects: List[Project] = [Project(p) for p in yaml]
            self._has_projects_key = False
        else:
            # TODO: Create new error type
            raise ClowderError(ClowderErrorType.YAML_UNKNOWN, "Wrong instance type for group")

    def get_yaml(self) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[dict, list]
        """

        if not self._has_projects_key:
            return [p.get_yaml() for p in self.projects]

        yaml = {"projects": [p.get_yaml() for p in self.projects]}

        if self.path is not None:
            yaml['path'] = str(self.path)
        if self.groups is not None:
            yaml['groups'] = str(self.groups)
        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()

        return yaml
