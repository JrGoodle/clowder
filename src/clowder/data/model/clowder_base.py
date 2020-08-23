# -*- coding: utf-8 -*-
"""Representation of clowder yaml loader

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional

from .clowder import Clowder
from .defaults import Defaults
from .source import Source
from .source_name import SourceName


class ClowderBase:
    """clowder yaml base class

    :ivar str name: Name of clowder
    :ivar Optional[Defaults] defaults: Name of clowder
    :ivar Optional[List[Source]] sources: Sources
    :ivar Clowder clowder: Clowder model
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
        self.clowder: Clowder = Clowder(yaml["clowder"])

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        yaml = {
            "name": self.name,
            "clowder": self.clowder.get_yaml()
        }

        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()
        if self.sources is not None:
            yaml['sources'] = {s.name.get_yaml(): s.get_yaml() for s in self.sources}

        return yaml
