# -*- coding: utf-8 -*-
"""Representation of clowder yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Union

from clowder.git import GitProtocol

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

    def __init__(self, name: str, yaml: Optional[Dict[str, str]] = None):
        """Source __init__

        :param str name: Source name
        :param Dict[str, str] yaml: Parsed YAML python object for source
        """

        self.name = name

        if yaml is None:
            self.url = None
            self.protocol = None
            return

        self.url = yaml['url']
        self.protocol = yaml.get(GitProtocol('protocol'), None)

    def get_yaml(self) -> Union[dict, str]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[dict, str]
        """

        if self.url is None and self.protocol is None:
            return self.name

        source = {'url': self.url}
        if self.protocol is not None:
            source['protocol'] = self.protocol

        return source
