"""Representation of clowder yaml secton

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Optional, Union
from pathlib import Path

from clowder.util.error import UnknownTypeError

from .defaults import Defaults
from .project import Project


class Section:
    """clowder yaml Section model class

    :ivar str name: Section name
    :ivar Optional[Path] path: Section path prefix
    :ivar Optional[List[str]] groups: Group names
    :ivar Optional[Defaults] defaults: Group defaults
    :ivar List[Project] projects: Group projects
    :ivar bool _has_projects_key: Whether the projects were listed under the 'projects' key in the yaml file
    """

    def __init__(self, name: str, yaml: Union[dict, List[Project]]):
        """Group __init__

        :param str name: Section name
        :param Union[dict, List[Project]] yaml: Parsed YAML python object for group
        :raise UnknownTypeError:
        """

        self.name: str = name

        if isinstance(yaml, dict):
            path = yaml.get('path', None)
            self.path: Optional[Path] = None if path is None else Path(path)
            self.groups: Optional[List[str]] = yaml.get('groups', None)
            defaults = yaml.get("defaults", None)
            self.defaults: Optional[Defaults] = None if defaults is None else Defaults(defaults)
            self.projects: List[Project] = [Project(p) for p in yaml["projects"]]
            self._has_projects_key: bool = True
        elif isinstance(yaml, list):
            self.path: Optional[Path] = None
            self.groups: Optional[List[str]] = None
            self.defaults: Optional[Defaults] = None
            self.projects: List[Project] = [Project(p) for p in yaml]
            self._has_projects_key: bool = False
        else:
            raise UnknownTypeError("Unknown group type")

    def get_yaml(self, resolved: bool = False) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :return: YAML python object
        """

        if not self._has_projects_key:
            return [p.get_yaml(resolved=resolved) for p in self.projects]

        yaml = {}

        if self.path is not None:
            yaml['path'] = str(self.path)
        if self.groups is not None:
            yaml['groups'] = self.groups
        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()

        yaml["projects"] = [p.get_yaml(resolved=resolved) for p in self.projects]

        return yaml
