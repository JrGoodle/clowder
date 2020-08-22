# -*- coding: utf-8 -*-
"""Representation of clowder yaml loader

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from .clowder import Clowder
from .defaults import Defaults
from .source import Source


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

        self.name = yaml["name"]
        self.defaults = Defaults(yaml["defaults"]) if "defaults" in yaml else None
        self.sources = [Source(name, source) for name, source in yaml["sources"].items()] if "sources" in yaml else None
        self.clowder = Clowder(yaml["clowder"])

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        yaml = {
            "name": self.name,
            "clowder": self.clowder
        }

        if self.defaults is not None:
            yaml['defaults'] = self.defaults.get_yaml()
        if self.sources is not None:
            yaml['source'] = self.sources = [s.get_yaml() for s in self.sources]

        return yaml
