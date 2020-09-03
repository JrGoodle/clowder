# -*- coding: utf-8 -*-
"""Source controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Set, Union

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
        """Returns all project names containing forks

        :param Optional[Source] source: Source to add
        """

        if self._has_been_validated:
            # TODO: Update error type
            message = "Called add_source() but SOURCE_CONTROLLER has already been validated"
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)
            LOG_DEBUG(message, err)
            raise err

        if source is None:
            return

        if isinstance(source, SourceName):
            self._source_names.add(source)
        elif isinstance(source, Source):
            self._source_names.add(source.name)
            self._sources[source.name] = source
        else:
            # TODO: Fix error type
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_REMOTE_NAME, "Wrong source type")
            LOG_DEBUG('Wrong source type', err)
            raise err

    def get_source(self, source: Union[SourceName, Source]) -> Source:
        """Returns Source by name

        :param SourceName source: Source name to return
        :return: Source with supplied name
        :rtype: Source
        """

        if not self._has_been_validated:
            # TODO: Update error type
            message = "Called get_source() but SOURCE_CONTROLLER has not been validated"
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)
            LOG_DEBUG(message, err)
            raise err

        if isinstance(source, SourceName):
            name = source
        elif isinstance(source, Source):
            name = source.name
        else:
            # TODO: Fix error type
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_REMOTE_NAME, "Wrong source type")
            LOG_DEBUG('Wrong source type', err)
            raise err

        if name not in self._sources:
            # TODO: Rename error to SOURCE_NOT_DEFINED
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, "No source defined")
            LOG_DEBUG('Failed to get source', err)
            raise err

        return self._sources[name]

    def get_default_protocol(self) -> str:
        """Returns Source by name

        :return: Source with supplied name
        :rtype: Source
        """

        if not self._has_been_validated:
            # TODO: Update error type
            message = "Called get_default_protocol() but SOURCE_CONTROLLER has not been validated"
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)
            LOG_DEBUG(message, err)
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
            # TODO: Update error messages to be more generic so missing source applies to defaults, project, upstream
            # message = fmt.error_source_not_found(self.defaults.source, ENVIRONMENT.clowder_yaml)
            message = "SOURCE NOT FOUND"
            err = ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)
            LOG_DEBUG('Failed to validate sources', err)
            raise err


SOURCE_CONTROLLER: SourceController = SourceController()
