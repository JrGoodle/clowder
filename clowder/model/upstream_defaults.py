"""Representation of clowder yaml upstream defaults

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Optional

from .source import SourceName


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
        self.source: Optional[SourceName] = None if source is None else SourceName(source)
        self.remote: Optional[str] = yaml.get("remote", None)

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        """

        yaml = {}

        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source

        return yaml
