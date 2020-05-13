# -*- coding: utf-8 -*-
"""Representation of clowder.yaml defaults

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class Defaults(object):
    """clowder.yaml Defaults model class

    :ivar str ref: Default ref
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
        self.ref = defaults.get("ref", "refs/heads/master")
        self.remote = defaults.get("remote", "origin")
        self.depth = defaults.get("depth", 0)
        self.recursive = defaults.get("recursive", False)
        self.timestamp_author = defaults.get("timestamp_author", None)

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
