"""Representation of clowder yaml upstream

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Optional, Union

from clowder.util.error import UnknownSourceError, UnknownTypeError

from .source import Source, SourceName


class Upstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar str path: Project relative path
    :ivar Optional[Union[Source, SourceName]] source: Upstream source
    :ivar Optional[str] remote: Upstream remote name
    """

    def __init__(self, yaml: Union[str, dict]):
        """Upstream __init__

        :param Union[str, dict] yaml: Parsed YAML python object for upstream
        :raise UnknownTypeError:
        """

        self._is_string = False

        if isinstance(yaml, str):
            self._is_string = True
            self.name: str = yaml
            self.remote: Optional[str] = None
            self.source: Optional[Union[Source, SourceName]] = None
            return

        if isinstance(yaml, dict):
            self.name: str = yaml['name']
            self.remote: Optional[str] = yaml.get('remote', None)

            self.source: Optional[Union[Source, SourceName]] = None
            source = yaml.get('source', None)
            if source is not None:
                if isinstance(source, SourceName):
                    self.source: Optional[Union[Source, SourceName]] = SourceName(source)
                elif isinstance(source, dict):
                    # Use upstream instance id as source name
                    name = SourceName(id(self))
                    self.source: Optional[Union[Source, SourceName]] = Source(name, source)
                else:
                    raise UnknownTypeError("Unknown source type")
            return

        raise UnknownTypeError("Unknown upstream type")

    def get_yaml(self) -> Union[str, dict]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :raise UnknownSourceError:
        """

        if self._is_string:
            return self.name

        yaml = {"name": self.name}

        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            if isinstance(self.source, SourceName):
                yaml['source'] = self.source
            elif isinstance(self.source, Source):
                yaml['source'] = self.source.get_yaml()
            else:
                raise UnknownSourceError('Unknown source type')

        return yaml
