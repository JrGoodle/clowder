# -*- coding: utf-8 -*-
"""Representation of clowder.yaml defaults

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.git.util import (
    format_git_branch,
    format_git_tag
)


class Defaults(object):
    """clowder.yaml Defaults model class

    :ivar str ref: Default ref
    :ivar Optional[str] branch: Default git branch
    :ivar Optional[str] tag: Default git tag
    :ivar Optional[str] commit: Default commit sha-1
    :ivar str remote: Default remote name
    :ivar str source: Default source name
    :ivar str protocol: Default git protocol
    :ivar int depth: Default depth
    :ivar bool recursive: Default recursive value
    :ivar str timestamp_author: Default timestamp author
    """

    def __init__(self, defaults: dict):
        """Defaults __init__

        :param dict defaults: Parsed YAML python object for defaults
        """

        self.protocol = defaults["protocol"]
        self.source = defaults["source"]
        self.remote = defaults.get("remote", "origin")
        self.depth = defaults.get("depth", 0)
        self.recursive = defaults.get("recursive", False)
        self.timestamp_author = defaults.get("timestamp_author", None)

        self.branch = defaults.get("branch", None)
        self.tag = defaults.get("tag", None)
        self.commit = defaults.get("commit", None)

        if self.branch is not None:
            self.ref = format_git_branch(self.branch)
        elif self.tag is not None:
            self.ref = format_git_tag(self.tag)
        elif self.commit is not None:
            self.ref = self.commit
        else:
            self.branch = 'master'
            self.ref = 'refs/heads/master'

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        defaults = {'ref': self.ref,
                    'recursive': self.recursive,
                    'remote': self.remote,
                    'source': self.source,
                    'depth': self.depth,
                    'protocol': self.protocol}

        if self.timestamp_author:
            defaults['timestamp_author'] = self.timestamp_author

        return defaults
