# -*- coding: utf-8 -*-
"""Representation of clowder yaml clowder

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union

from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

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
            # TODO: Create new error type
            raise ClowderError(ClowderErrorType.YAML_UNKNOWN, "Wrong instance type for group")

    def get_yaml(self) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[dict, list]
        """

        if self.projects is not None:
            return [p.get_yaml() for p in self.projects]
        if self.groups is not None:
            return {g.name: g.get_yaml() for g in self.groups}

        message = "Clowder model created without projects or groups"
        err = ClowderError(ClowderErrorType.CLOWDER_YAML_UNKNOWN, message)
        LOG_DEBUG(message, err)
        raise err
