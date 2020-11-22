"""Source controller class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Dict, Optional, Set, Union

from clowder.git import GitProtocol
# from clowder.logging import LOG
from clowder.util.error import SourcesValidatedError, UnknownSourceError, UnknownTypeError

from .model import Source
from .model import SourceName

GITHUB: SourceName = SourceName("github")
GITLAB: SourceName = SourceName("gitlab")
BITBUCKET: SourceName = SourceName("bitbucket")
GITHUB_YAML: Dict[str, str] = {'url': 'github.com'}
GITLAB_YAML: Dict[str, str] = {'url': 'gitlab.com'}
BITBUCKET_YAML: Dict[str, str] = {'url': 'bitbucket.org'}


class SourceController(object):
    """Class encapsulating project information from clowder yaml for controlling clowder

    :ivar Optional[str] protocol_override: The protocol to override sources without an explicitly specified protcol
    """

    def __init__(self):
        """SourceController __init__"""

        self._has_been_validated: bool = False
        self._source_names: Set[SourceName] = {GITHUB, GITLAB, BITBUCKET}
        # TODO: Make into @property method and check validation
        self.protocol_override: Optional[GitProtocol] = None

        self._sources: Dict[SourceName, Source] = {
            GITHUB: Source(GITHUB, GITHUB_YAML),
            GITLAB: Source(GITLAB, GITLAB_YAML),
            BITBUCKET: Source(BITBUCKET, BITBUCKET_YAML)
        }

    def add_source(self, source: Optional[Union[Source, SourceName]]):
        """Register source with controller

        :param Optional[Union[Source, SourceName]] source: Source to add
        :raise SourcesValidatedError:
        :raise UnknownTypeError:
        """

        if self._has_been_validated:
            raise SourcesValidatedError('Called add_source() but SOURCE_CONTROLLER has already been validated')

        if source is None:
            return

        if isinstance(source, SourceName):
            self._source_names.add(source)
        elif isinstance(source, Source):
            self._source_names.add(source.name)
            self._sources[source.name] = source
        else:
            raise UnknownTypeError('Unknown source type')

    def get_source(self, source: Union[SourceName, Source]) -> Source:
        """Returns Source by name

        :param Union[SourceName, Source] source: Source to return
        :return: Source with supplied name
        :raise SourcesValidatedError:
        :raise UnknownTypeError:
        :raise UnknownSourceError:
        """

        if not self._has_been_validated:
            raise SourcesValidatedError("Called get_source() but SOURCE_CONTROLLER has not been validated")

        if isinstance(source, SourceName):
            source_name = source
        elif isinstance(source, Source):
            source_name = source.name
        else:
            raise UnknownTypeError("Unknown source type")

        if source_name not in self._sources:
            raise UnknownSourceError(f"Unknown source: {source_name}")

        return self._sources[source_name]

    def get_default_protocol(self) -> GitProtocol:
        """Returns default protocol

        :return: Default git protocol
        :raise SourcesValidatedError:
        """

        if not self._has_been_validated:
            raise SourcesValidatedError("Called get_default_protocol() but SOURCE_CONTROLLER has not been validated")

        if self.protocol_override is not None:
            return self.protocol_override
        else:
            return GitProtocol.SSH

    def validate_sources(self) -> None:
        """Validate sources: check for unknown names

        :raise UnknownSourceError:
        """

        self._has_been_validated = True
        if not any([s.name == name for name, s in self._sources.items()]):
            raise UnknownSourceError('Failed to validate sources - source not defined')


SOURCE_CONTROLLER: SourceController = SourceController()
