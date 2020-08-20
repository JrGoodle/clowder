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

    def __init__(self, defaults: dict):
        """Defaults __init__

        :param dict defaults: Parsed YAML python object for defaults
        """

        self.protocol = GitProtocol(defaults.get("protocol", "ssh"))
        self._protocol: str = defaults.get("protocol", None)

        self.source: str = defaults.get("source", "github")
        self._source: str = defaults.get("source", None)

        self.remote: str = defaults.get("remote", "origin")
        self._remote: Optional[str] = defaults.get("remote", None)

        self.git_settings = GitSettings(git_settings=defaults.get("git", None))
        git_settings = defaults.get("git", None)
        if git_settings is not None:
            self._git_settings: Optional[GitSettingsImpl] = GitSettingsImpl(git_settings)
        else:
            self._git_settings: Optional[GitSettingsImpl] = None

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
            self._branch: Optional[str] = defaults.get("branch", None)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
            self._tag: Optional[str] = defaults.get("tag", None)
        elif self._commit is not None:
            self.ref = self._commit
            self._commit: Optional[str] = defaults.get("commit", None)
        else:
            self.ref = format_git_branch('master')

        self.timestamp_author: Optional[str] = defaults.get("timestamp_author", None)

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
