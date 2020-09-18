# -*- coding: utf-8 -*-
"""Source controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Set, Union

import clowder.util.formatting as fmt
from clowder.logging import LOG_DEBUG
from clowder.error import ClowderError, ClowderErrorType

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
        self.protocol_override: Optional[str] = None  # TODO: Make into @property method and check validation
        self._source_names: Set[SourceName] = {GITHUB, GITLAB, BITBUCKET}

        self._sources: Dict[SourceName, Source] = {
            GITHUB: Source(GITHUB, GITHUB_YAML),
            GITLAB: Source(GITLAB, GITLAB_YAML),
            BITBUCKET: Source(BITBUCKET, BITBUCKET_YAML)
        }

    def add_source(self, source: Optional[Union[Source, SourceName]]):
        """Register source with controller

        :param Optional[Union[Source, SourceName]] source: Source to add
        """

        if self._has_been_validated:
            err = ClowderError(ClowderErrorType.SOURCES_ALREADY_VALIDATED, fmt.error_sources_already_validated())
            LOG_DEBUG("Called add_source() but SOURCE_CONTROLLER has already been validated", err)
            raise err

        if source is None:
            return

        if isinstance(source, SourceName):
            self._source_names.add(source)
        elif isinstance(source, Source):
            self._source_names.add(source.name)
            self._sources[source.name] = source
        else:
            err = ClowderError(ClowderErrorType.WRONG_SOURCE_TYPE, fmt.error_wrong_source_type())
            LOG_DEBUG('Wrong source type', err)
            raise err

    def get_source(self, source: Union[SourceName, Source]) -> Source:
        """Returns Source by name

        :param Union[SourceName, Source] source: Source to return
        :return: Source with supplied name
        :rtype: Source
        """

        if not self._has_been_validated:
            err = ClowderError(ClowderErrorType.SOURCES_NOT_VALIDATED, fmt.error_source_not_validated())
            LOG_DEBUG("Called get_source() but SOURCE_CONTROLLER has not been validated", err)
            raise err

        if isinstance(source, SourceName):
            source_name = source
        elif isinstance(source, Source):
            source_name = source.name
        else:
            err = ClowderError(ClowderErrorType.WRONG_SOURCE_TYPE, fmt.error_wrong_source_type())
            LOG_DEBUG('Wrong source type', err)
            raise err

        if source_name not in self._sources:
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND,
                               fmt.error_source_not_defined(source_name.name))
            LOG_DEBUG('Failed to get source', err)
            raise err

        return self._sources[source_name]

    def get_default_protocol(self) -> str:
        """Returns Source by name

        :return: Default git protocol
        :rtype: str
        """

        if not self._has_been_validated:
            err = ClowderError(ClowderErrorType.SOURCES_NOT_VALIDATED, fmt.error_source_not_validated())
            LOG_DEBUG("Called get_default_protocol() but SOURCE_CONTROLLER has not been validated", err)
            raise err

        if self.protocol_override is not None:
            return self.protocol_override
        else:
            return 'ssh'

    def validate_sources(self) -> None:
        """Validate sources: check for unknown names

        :raises
        """

        self._has_been_validated = True
        if not any([s.name == name for name, s in self._sources.items()]):
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, fmt.error_source_not_defined())
            LOG_DEBUG('Failed to validate sources', err)
            raise err


SOURCE_CONTROLLER: SourceController = SourceController()
