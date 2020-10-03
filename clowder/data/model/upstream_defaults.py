# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream defaults

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional

from .source_name import SourceName


class UpstreamDefaults:
    """clowder yaml UpstreamDefaults model class

    :ivar Optional[SourceName] source: Default source name
    :ivar Optional[str] remote: Default remote name
    """

    def __init__(self, yaml: dict):
        """Defaults __init__

        :param dict yaml: Parsed YAML python object for upstream defaults
        """

        source = yaml.get("source", None)
        self.source: Optional[SourceName] = SourceName(source) if source is not None else None
        self.remote: Optional[str] = yaml.get("remote", None)

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        yaml = {}

        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source.get_yaml()

        return yaml
