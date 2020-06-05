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

from .git_settings import GitSettings, GitSettingsImpl


class DefaultsImpl(object):
    """clowder yaml Defaults model impl class

    :ivar str source: Default source name
    :ivar GitProtocol protocol: Default git protocol
    :ivar GitSettings git_settings: Custom git settings
    :ivar str timestamp_author: Default timestamp author
    """

    def __init__(self, defaults: dict):
        """Defaults __init__

        :param dict defaults: Parsed YAML python object for defaults
        """

        self.protocol = GitProtocol(defaults["protocol"])
        self._source: str = defaults.get("source", None)

        self._remote: Optional[str] = defaults.get("remote", None)
        self._branch: Optional[str] = defaults.get("branch", None)
        self._tag: Optional[str] = defaults.get("tag", None)
        self._commit: Optional[str] = defaults.get("commit", None)
        self.timestamp_author: Optional[str] = defaults.get("timestamp_author", None)

        git_settings = defaults.get("git", None)
        if git_settings is not None:
            self._git_settings = GitSettingsImpl(git_settings)
        else:
            self._git_settings = None

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        defaults = {'protocol': self.protocol.value}

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


class Defaults(DefaultsImpl):
    """clowder yaml Defaults model class

    :ivar str ref: Default ref
    :ivar str remote: Default remote name
    :ivar GitSettings git_settings: Custom git settings
    :ivar Optional[str] branch: Default git branch
    :ivar Optional[str] tag: Default git tag
    :ivar Optional[str] commit: Default commit sha-1
    """

    def __init__(self, defaults: dict):
        """Defaults __init__

        :param dict defaults: Parsed YAML python object for defaults
        """

        super().__init__(defaults)

        self.source: str = defaults.get("source", None)
        self.remote: str = defaults.get("remote", "origin")
        self.git_settings = GitSettings(git_settings=defaults.get("git", None))

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self.ref = format_git_branch('master')
