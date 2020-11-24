"""Representation of clowder yaml clowder

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Optional, Union

from clowder.util.error import InvalidYamlError, UnknownTypeError

from .section import Section
from .project import Project


class Clowder:
    """clowder yaml Clowder model class

    :ivar Optional[List[Project]] projects: Projects
    :ivar Optional[List[Group]] sections: Groups
    """

    def __init__(self, yaml: Union[dict, List[Project]]):
        """Upstream __init__

        :param Union[dict, List[Project]] yaml: Parsed YAML python object for clowder
        """

        if isinstance(yaml, dict):
            self.projects: Optional[List[Project]] = None
            self.sections: Optional[List[Section]] = [Section(name, section) for name, section in yaml.items()]
        elif isinstance(yaml, list):
            self.projects: Optional[List[Project]] = [Project(p) for p in yaml]
            self.sections: Optional[List[Section]] = None
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
        elif self.sections is not None:
            return {s.name: s.get_yaml(resolved=resolved) for s in self.sections}
        else:
            raise InvalidYamlError('Clowder model created without projects or groups')
