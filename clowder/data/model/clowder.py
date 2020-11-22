"""Representation of clowder yaml clowder

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Optional, Union

from clowder.util.error import InvalidYamlError, UnknownTypeError

from .group import Group
from .project import Project


class Clowder:
    """clowder yaml Clowder model class

    :ivar Optional[List[Project]] projects: Projects
    :ivar Optional[List[Group]] groups: Groups
    """

    def __init__(self, yaml: Union[dict, List[Project]]):
        """Upstream __init__

        :param Union[dict, List[Project]] yaml: Parsed YAML python object for clowder
        """

        if isinstance(yaml, dict):
            self.projects: Optional[List[Project]] = None
            self.groups: Optional[List[Group]] = [Group(name, group) for name, group in yaml.items()]
        elif isinstance(yaml, list):
            self.projects: Optional[List[Project]] = [Project(p) for p in yaml]
            self.groups: Optional[List[Group]] = None
        else:
            raise UnknownTypeError("Unknown group type")

    def get_yaml(self, resolved: bool = False) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :param bool resolved: Whether to get resolved commit hashes
        :return: YAML python object
        :raise InvalidYamlError:
        """

        if self.projects is not None:
            return [p.get_yaml(resolved=resolved) for p in self.projects]
        elif self.groups is not None:
            return {g.name: g.get_yaml(resolved=resolved) for g in self.groups}
        else:
            raise InvalidYamlError('Clowder model created without projects or groups')
