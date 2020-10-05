# -*- coding: utf-8 -*-
"""Representation of clowder yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.git_project.util import (
    format_git_branch,
    format_git_tag
)
from clowder.logging import LOG_DEBUG

from .upstream import Upstream
from .git_settings import GitSettings
from .source import Source
from .source_name import SourceName


class Project:
    """clowder yaml Project model class

    :ivar Optional[int] resolved_project_id: Identifier for ResolvedProject instance created from this Project
    :ivar str name: Project name
    :ivar Optional[Path] path: Project relative path
    :ivar Optional[str] branch: Git branch
    :ivar Optional[str] tag: Git tag
    :ivar Optional[str] commit: Git commit
    :ivar Optional[List[str]] groups: Groups project belongs to
    :ivar Optional[str] remote: Project remote name
    :ivar Optional[Union[Source, SourceName]] source: Project source
    :ivar Optional[GitSettings] git_settings: Custom git settings
    :ivar Optional[Upstream] upstream: Project's associated Upstream
    """

    def __init__(self, yaml: Union[dict, str]):
        """Project __init__

        :param Union[dict, str] yaml: Parsed YAML python object for project
        """

        self.resolved_project_id: Optional[int] = None
        self._is_string = False

        if isinstance(yaml, str):
            self._is_string = True
            self.name: str = yaml
            self.branch: Optional[str] = None
            self.tag: Optional[str] = None
            self.commit: Optional[str] = None
            self.groups: Optional[List[str]] = None
            self.remote: Optional[str] = None
            self.path: Optional[Path] = None
            self.source: Optional[Union[Source, SourceName]] = None
            self.git_settings: Optional[GitSettings] = None
            self.upstream: Optional[Upstream] = None
            return

        self.name: str = yaml['name']
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)
        self.groups: Optional[List[str]] = yaml.get('groups', None)
        self.remote: Optional[str] = yaml.get('remote', None)

        path = yaml.get('path', None)
        self.path: Optional[Path] = Path(path) if path is not None else None

        self.source: Optional[Union[Source, SourceName]] = None
        source = yaml.get('source', None)
        if source is not None:
            if isinstance(source, str):
                self.source: Optional[Union[Source, SourceName]] = SourceName(source)
            elif isinstance(source, dict):
                # Use project instance id as source name
                name = SourceName(str(id(self)))
                self.source: Optional[Union[Source, SourceName]] = Source(name, source)
            else:
                err = ClowderError(ClowderErrorType.WRONG_SOURCE_TYPE, fmt.error_wrong_source_type())
                LOG_DEBUG('Wrong source type', err)
                raise err

        git = yaml.get('git', None)
        self.git_settings: Optional[GitSettings] = GitSettings(git) if git is not None else None

        upstream = yaml.get('upstream', None)
        self.upstream: Optional[Upstream] = Upstream(upstream) if upstream is not None else None

    def get_formatted_ref(self) -> Optional[str]:
        """Return formatted git ref

        :return: Formatted git ref
        :rtype: Optional[str]
        """

        if self.branch is not None:
            return format_git_branch(self.branch)
        elif self.tag is not None:
            return format_git_tag(self.tag)
        elif self.commit is not None:
            return self.commit
        else:
            return None

    def get_yaml(self, resolved: bool = False) -> Union[dict, str]:
        """Return python object representation for saving yaml

        :param bool resolved: Whether to get resolved commit hashes
        :return: YAML python object
        :rtype: Union[dict, str]
        """

        from clowder.clowder_controller import CLOWDER_CONTROLLER

        if self._is_string:
            if not resolved:
                return self.name

            return {
                "name": self.name,
                "commit": CLOWDER_CONTROLLER.get_project_sha(self.resolved_project_id)
            }

        yaml = {"name": self.name}

        if self.path is not None:
            yaml['path'] = str(self.path)
        if resolved:
            yaml['commit'] = CLOWDER_CONTROLLER.get_project_sha(self.resolved_project_id)
        else:
            if self.branch is not None:
                yaml['branch'] = self.branch
            if self.tag is not None:
                yaml['tag'] = self.tag
            if self.commit is not None:
                yaml['commit'] = self.commit
        if self.groups is not None:
            yaml['groups'] = self.groups
        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source.get_yaml()
        if self.git_settings is not None:
            yaml['git'] = self.git_settings.get_yaml()
        if self.upstream is not None:
            yaml['upstream'] = self.upstream.get_yaml()

        return yaml
