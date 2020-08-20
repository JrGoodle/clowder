# -*- coding: utf-8 -*-
"""Representation of clowder yaml defaults

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional

from clowder.git import GitProtocol
from clowder.git.util import (
    format_git_branch,
    format_git_tag
)

from .git_settings import GitSettings


class Defaults:
    """clowder yaml Defaults model class

    :ivar Optional[str] source: Default source name
    :ivar Optional[GitProtocol] protocol: Default git protocol
    :ivar Optional[str] remote: Default remote name
    :ivar Optional[GitSettings] git_settings: Custom git settings
    :ivar Optional[str] branch: Default git branch
    :ivar Optional[str] tag: Default git tag
    :ivar Optional[str] commit: Default commit sha-1
    """

    def __init__(self, yaml: dict):
        """Defaults __init__

        :param dict yaml: Parsed YAML python object for defaults
        """

        protocol = yaml.get("protocol", None)
        self.protocol: Optional[GitProtocol] = GitProtocol(protocol) if protocol is not None else None
        self.source: Optional[str] = yaml.get("source", None)
        self.remote: Optional[str] = yaml.get("remote", None)
        git = yaml.get("git", None)
        self.git_settings = GitSettings(git) if git is not None else None
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)


    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        defaults = {}

        if self._protocol is not None:
            defaults['protocol'] = self._protocol
        if self._source is not None:
            defaults['source'] = self._source
        if self._remote is not None:
            defaults['remote'] = self._remote
        if self._git_settings is not None:
            defaults['git'] = self._git_settings.get_yaml()
        if self._branch is not None:
            defaults['branch'] = self._branch
        elif self._tag is not None:
            defaults['tag'] = self._tag
        elif self._commit is not None:
            defaults['commit'] = self._commit

        if self.timestamp_author is not None:
            defaults['timestamp_author'] = self.timestamp_author

        return defaults
