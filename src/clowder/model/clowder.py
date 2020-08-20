# -*- coding: utf-8 -*-
"""Representation of clowder yaml clowder

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, Tuple, TYPE_CHECKING

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_git_branch,
    format_git_tag,
    git_url
)

from .defaults import Defaults
from .source import Source


class Clowder:
    """clowder yaml Clowder model class

    :ivar Optional[List[Project]] projects: Projects
    :ivar Optional[List[Group]] groups: Groups
    """

    def __init__(self, upstream: dict, project: 'Project', sources: Tuple[Source, ...], defaults: Defaults):
        """Upstream __init__

        :param dict upstream: Parsed YAML python object for upstream
        :param Project project: Parent project
        :param Tuple[Source, ...] sources: List of Source instances
        :param Defaults defaults: Defaults instance
        """

        # TODO: Implement

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        return {}
