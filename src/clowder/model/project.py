# -*- coding: utf-8 -*-
"""Representation of clowder yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from functools import wraps
from pathlib import Path
from typing import List, Optional, Tuple

from termcolor import colored, cprint

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git import ProjectRepo, ProjectRepoRecursive
from clowder.git.util import (
    existing_git_repository,
    format_git_branch,
    format_git_tag,
    git_url
)
from clowder.logging import LOG_DEBUG
from clowder.util.connectivity import is_offline
from clowder.util.execute import execute_forall_command

from .defaults import Defaults
from .upstream import Upstream
from .git_settings import GitSettings
from .source import Source


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not Path(instance.full_path() / '.git').is_dir():
            cprint(" - Project missing", 'red')
            return
        return func(*args, **kwargs)

    return wrapper


class Project:
    """clowder yaml Project model class

    :ivar str name: Project name
    :ivar Optional[Path] path: Project relative path
    :ivar Optional[List[str]] groups: Groups project belongs to
    :ivar Optional[str] remote: Project remote name
    :ivar Optional[Source] source: Project source
    :ivar Optional[GitSettings] git_settings: Custom git settings
    :ivar Optional[Upstream] upstream: Project's associated Upstream
    """

    def __init__(self, yaml: dict):
        """Project __init__

        :param dict yaml: Parsed YAML python object for project
        """

        self.name: str = yaml['name']
        self.path: Optional[str] = yaml.get('path', None)
        self.remote: Optional[str] = yaml.get('remote', None)
        self.source: Optional[str] = yaml.get('source', None)
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)
        self.groups: Optional[List[str]] = yaml.get('groups', None)

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        project = {'name': self.name}

        if self._path is not None:
            project['path'] = self._path
        if self._remote is not None:
            project['remote'] = self._remote
        if self._source is not None:
            project['source'] = self._source
        if self._groups is not None:
            project['groups'] = self._groups
        if self._fork is not None:
            project['upstream'] = self._fork.get_yaml(resolved_sha=resolved_sha)
        if self._git_settings is not None:
            project['git'] = self._git_settings.get_yaml()
        if self._timestamp_author is not None:
            project['timestamp_author'] = self._timestamp_author

        if resolved_sha is None:
            if self._branch is not None:
                project['branch'] = self._branch
            elif self._tag is not None:
                project['tag'] = self._tag
            elif self._commit is not None:
                project['commit'] = self._commit
        else:
            project['commit'] = resolved_sha

        return project
