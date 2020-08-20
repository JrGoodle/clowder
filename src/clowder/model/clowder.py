# -*- coding: utf-8 -*-
"""Representation of clowder yaml clowder

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Union

from clowder.error import ClowderError, ClowderErrorType

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

        # TODO: Implement

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        return {}
