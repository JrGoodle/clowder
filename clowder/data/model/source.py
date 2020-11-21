"""Representation of clowder yaml source

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Dict, Optional

from clowder.git_project import GitProtocol

SourceName = str


class Source:
    """clowder yaml Source model class

    :ivar SourceName name: Source name
    :ivar str url: Git project url
    :ivar Optional[GitProtocol] protocol: Git protocol
    """

    def __init__(self, name: SourceName, yaml: Dict[str, str]):
        """Source __init__

        :param str name: Source name
        :param Dict[str, str] yaml: Parsed YAML python object for source
        """

        self.name: SourceName = name
        self.url: str = yaml['url']
        protocol = yaml.get("protocol", None)
        self.protocol: Optional[GitProtocol] = None if protocol is None else GitProtocol(protocol)

    def get_yaml(self) -> Dict[str, str]:
        """Return python object representation for saving yaml

        :return: YAML python object
        """

        source = {"url": self.url}

        if self.protocol is not None:
            source['protocol'] = self.protocol.value

        return source
