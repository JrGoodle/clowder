# -*- coding: utf-8 -*-
"""Representation of clowder yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional

from clowder.git import GitProtocol

from .defaults import Defaults


class SourceImpl(object):
    """clowder yaml SourceImpl model class

    :ivar str name: Source name
    :ivar str url: Source url
    """

    def __init__(self, source: dict):
        """Source __init__

        :param dict source: Parsed YAML python object for source
        """

        self.name = source['name']
        self.url = source['url']
        self._protocol = source.get('protocol', None)

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        source = {'name': self.name,
                  'url': self.url}

        if self._protocol is not None:
            source['protocol'] = self._protocol

        return source


class Source(SourceImpl):
    """clowder yaml Source model class

    :ivar 'GitProtocol' protocol Git protocol
    """

    def __init__(self, source: dict, defaults: Defaults):
        """Source __init__

        :param dict source: Parsed YAML python object for source
        :param Defaults defaults: Defaults instance
        """

        super().__init__(source)

        self.protocol = GitProtocol(source.get('protocol', defaults.protocol))

    def update_protocol(self, protocol: Optional[str]):
        """Updates git protocol if it wasn't explicitly set for this source in the clowder yaml file

        :param Optional[str] protocol: Git protocol to use for cloning
        """

        if protocol is not None and self._protocol is None:
            self.protocol = GitProtocol(protocol)
