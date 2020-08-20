# -*- coding: utf-8 -*-
"""Representation of clowder yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional

from clowder.git import GitProtocol

from .defaults import Defaults

DEFAULT_SOURCES: Dict[str, Dict[str, str]] = {
    'github': {
        'url': 'github.com'
    },
    'gitlab': {
        'url': 'gitlab.com'
    },
    'bitbucket': {
        'url': 'bitbucket.org'
    }
}


class Source:
    """clowder yaml Source model class

    :ivar str name: Source name
    :ivar Optional[str] url: Source url
    :ivar Optional[GitProtocol] protocol: Git protocol
    """

    def __init__(self, name: str, source: Dict[str, str], defaults: Defaults, is_custom: bool):
        """Source __init__

        :param str name: Source name
        :param Dict[str, str] source: Parsed YAML python object for source
        :param Defaults defaults: Defaults instance
        :param bool is_custom: Whether this is a custom user-defined source
        """

        self.name = name
        self.url = source['url']
        self._protocol = source.get('protocol', None)

        self.is_custom = is_custom
        self.protocol = GitProtocol(source.get('protocol', defaults.protocol))

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        source = {'url': self.url}

        if self._protocol is not None:
            source['protocol'] = self._protocol

        return source

    def update_protocol(self, protocol: Optional[str]):
        """Updates git protocol if it wasn't explicitly set for this source in the clowder yaml file

        :param Optional[str] protocol: Git protocol to use for cloning
        """

        if protocol is not None and self._protocol is None:
            self.protocol = GitProtocol(protocol)
