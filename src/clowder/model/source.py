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

    def __init__(self, name: str, yaml: Optional[Dict[str, str]]):
        """Source __init__

        :param str name: Source name
        :param Dict[str, str] yaml: Parsed YAML python object for source
        """

        self.name = name
        self.url = yaml['url']
        self.protocol = yaml.get(GitProtocol('protocol'), None)

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        source = {'url': self.url}

        if self._protocol is not None:
            source['protocol'] = self._protocol

        return source
