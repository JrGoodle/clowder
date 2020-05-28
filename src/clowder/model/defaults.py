# -*- coding: utf-8 -*-
"""Representation of clowder yaml defaults

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.git import GitProtocol
from clowder.git.util import (
    format_git_branch,
    format_git_tag
)

from .git_settings import GitSettings


class Defaults(object):
    """clowder yaml Defaults model class

    :ivar str ref: Default ref
    :ivar Optional[str] branch: Default git branch
    :ivar Optional[str] tag: Default git tag
    :ivar Optional[str] commit: Default commit sha-1
    :ivar str remote: Default remote name
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
        self.source = defaults["source"]

        self._remote = defaults.get("remote", None)
        self.remote = defaults.get("remote", "origin")

        self.timestamp_author = defaults.get("timestamp_author", None)

        git_settings = defaults.get("git", None)
        if git_settings is not None:
            self.git_settings = GitSettings(git_settings)
        else:
            self.git_settings = None

        self._branch = defaults.get("branch", None)
        self._tag = defaults.get("tag", None)
        self._commit = defaults.get("commit", None)

        if self._branch is not None:
            self.branch = self._branch
            self.ref = format_git_branch(self.branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self.ref = format_git_branch('master')

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        defaults = {'source': self.source,
                    'protocol': self.protocol.value}

        if self._remote is not None:
            defaults['remote'] = self._remote
        if self.git_settings is not None:
            defaults['git'] = self.git_settings.get_yaml()
        if self._branch is not None:
            defaults['branch'] = self.branch
        elif self._tag is not None:
            defaults['tag'] = self._tag
        elif self._commit is not None:
            defaults['commit'] = self._commit

        if self.timestamp_author:
            defaults['timestamp_author'] = self.timestamp_author

        return defaults
