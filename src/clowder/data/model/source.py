# -*- coding: utf-8 -*-
"""Representation of clowder yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Union


class Source:
    """clowder yaml Source model class

    :ivar str name: Source name
    :ivar Optional[str] url: Source url
    :ivar Optional[str] protocol: Git protocol
    """

    def __init__(self, name: str, yaml: Union[str, Dict[str, str]] = None):
        """Source __init__

        :param str name: Source name
        :param Dict[str, str] yaml: Parsed YAML python object for source
        """

        if yaml is None:
            self.name: str = name
            self.url: Optional[str] = None
            self.protocol: Optional[str] = None
            return

        self.name: str = name
        self.url: Optional[str] = yaml['url']
        protocol = yaml.get('protocol', None)
        self.protocol: Optional[str] = protocol if protocol is not None else None

    def get_yaml(self) -> Union[dict, str]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[dict, str]
        """

        if self._is_reference():
            return self.name

        source = {'url': self.url}
        if self.protocol is not None:
            source['protocol'] = self.protocol

        return source

    def _is_reference(self) -> bool:
        """

        :return: YAML python object
        :rtype: bool
        """

        return self.url is None and self.protocol is None
