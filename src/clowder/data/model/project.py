# -*- coding: utf-8 -*-
"""Representation of clowder yaml project

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Optional

from clowder.git.util import (
    format_git_branch,
    format_git_tag
)

from .upstream import Upstream
from .git_settings import GitSettings
from .source import Source


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
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)
        self.groups: Optional[List[str]] = yaml.get('groups', None)
        self.remote: Optional[str] = yaml.get('remote', None)

        path = yaml.get('path', None)
        self.path: Optional[Path] = Path(path) if path is not None else None

        source = yaml.get('source', None)
        self.source: Optional[Source] = Source(source) if source is not None else None

        git = yaml.get('git', None)
        self.git_settings: Optional[GitSettings] = GitSettings(git) if git is not None else None

        upstream = yaml.get('upstream', None)
        self.upstream: Optional[Upstream] = Upstream(upstream) if upstream is not None else None

    def get_formatted_ref(self) -> Optional[str]:
        """Return formatted git ref

        :return: Formatted git ref
        :rtype: str
        """

        if self.branch is not None:
            return format_git_branch(self.branch)
        elif self.tag is not None:
            return format_git_tag(self.tag)
        elif self.commit is not None:
            return self.commit
        else:
            return None

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        yaml = {"name": self.name}

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
        if self.path is not None:
            yaml['path'] = str(self.path)
        if self.source is not None:
            yaml['source'] = self.source.get_yaml()
        if self.git_settings is not None:
            yaml['git'] = self.git_settings.get_yaml()
        if self.upstream is not None:
            yaml['upstream'] = self.upstream.get_yaml()

        return yaml
