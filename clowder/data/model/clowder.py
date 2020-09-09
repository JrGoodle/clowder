# -*- coding: utf-8 -*-
"""Representation of clowder yaml clowder

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union

import clowder.util.formatting as fmt
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
            err = ClowderError(ClowderErrorType.WRONG_GROUP_TYPE, fmt.error_wrong_group_type())
            LOG_DEBUG("Wrong instance type for group", err)
            raise err

    def get_yaml(self, resolved: bool = False) -> Union[dict, list]:
        """Return python object representation for saving yaml

        :param bool resolved: Whether to get resolved commit hashes
        :return: YAML python object
        :rtype: Union[dict, list]
        """

        if self.projects is not None:
            return [p.get_yaml(resolved=resolved) for p in self.projects]
        if self.groups is not None:
            return {g.name: g.get_yaml(resolved=resolved) for g in self.groups}

        message = "Clowder model created without projects or groups"
        err = ClowderError(ClowderErrorType.CLOWDER_YAML_UNKNOWN, message)
        LOG_DEBUG(message, err)
        raise err
