# -*- coding: utf-8 -*-
"""Source controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Set, Union

from clowder.error import ClowderError, ClowderErrorType

from .model import Source

GITHUB = "github"
GITLAB = "gitlab"
BITBUCKET = "bitbucket"
GITHUB_YAML: Dict[str, str] = {'url': 'github.com'}
GITLAB_YAML: Dict[str, str] = {'url': 'gitlab.com'}
BITBUCKET_YAML: Dict[str, str] = {'url': 'bitbucket.org'}


class SourceController(object):
    """Class encapsulating project information from clowder yaml for controlling clowder"""

    def __init__(self):
        """SourceController __init__"""

        self.protocol_override = None
        self._source_names: Set[str] = set()

        self._sources: Dict[str, Source] = {
            GITHUB: Source(GITHUB, GITHUB_YAML),
            GITLAB: Source(GITLAB, GITLAB_YAML),
            BITBUCKET: Source(BITBUCKET, BITBUCKET_YAML)
        }

    def add_source(self, source: Optional[Union[Source, str]]):
        """Returns all project names containing forks

        :param Optional[Source] source: Source to add
        """

        if source is None:
            return

        if isinstance(source, str):
            self._source_names.add(source)
            return

        self._sources[source.name] = source

    def get_source(self, name: str) -> Source:
        """Returns Source by name

        :param str name: Source name to return
        :return: Source with supplied name
        :rtype: Source
        """

        if name not in self._sources:
            # TODO: Rename error to SOURCE_NOT_DEFINED
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, "No source defined")

        return self._sources[name]

    def get_default_protocol(self) -> str:
        """Returns Source by name

        :param str name: Source name to return
        :return: Source with supplied name
        :rtype: Source
        """

        if self.protocol_override is not None:
            return self.protocol_override
        else:
            return 'ssh'

    def validate_sources(self) -> None:
        """Validate sources: check for unknown names

        :raises
        """

        if not any([s.name == name for name, s in self._sources.items()]):
            # TODO: Update error messages to be more generic so missing source applies to defaults, project, upstream
            # message = fmt.error_source_not_found(self.defaults.source, ENVIRONMENT.clowder_yaml)
            message = "SOURCE NOT FOUND"
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)


SOURCE_CONTROLLER: SourceController = SourceController()
