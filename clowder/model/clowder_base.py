"""Representation of clowder yaml loader

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Optional

from clowder.util.git import Protocol

from .clowder import Clowder
from .defaults import Defaults
from .source import Source, SourceName


class ClowderBase:
    """clowder yaml base class

    :ivar str name: Name of clowder
    :ivar Optional[Defaults] defaults: Name of clowder
    :ivar Optional[List[Source]] sources: Sources
    :ivar Clowder clowder: Clowder model
    :ivar Optional[Protocol] protocol: Git protocol
    """

    def __init__(self, yaml: dict):
        """Upstream __init__

        :param dict yaml: Parsed yaml dict
        """

        self.name: str = yaml["name"]
        self.defaults: Optional[Defaults] = Defaults(yaml["defaults"]) if "defaults" in yaml else None
        self.sources: Optional[List[Source]] = None
        if "sources" in yaml:
            self.sources: Optional[List[Source]] = [Source(SourceName(name), source)
                                                    for name, source in yaml["sources"].items()]
        protocol = yaml.get("protocol", None)
        self.protocol: Optional[Protocol] = None if protocol is None else Protocol(protocol)
        self.clowder: Clowder = Clowder(yaml["clowder"])

    def get_yaml(self, resolved: bool = False) -> dict:
        """Return python object representation for saving yaml

        :param bool resolved: Whether to get resolved commit hashes
        :return: YAML python object
        """

        yaml = {
            "name": self.name
        }

        if self.protocol is not None:
            yaml['protocol'] = self.protocol.value
        if self.sources is not None:
            yaml['sources'] = {s.name: s.get_yaml() for s in self.sources}
        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()

        yaml["clowder"] = self.clowder.get_yaml(resolved=resolved)

        return yaml
