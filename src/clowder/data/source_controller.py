# -*- coding: utf-8 -*-
"""Source controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Set

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

        self._source_names: Set[str] = set()

        self._sources: Dict[str, Source] = {
            GITHUB: Source(GITHUB, GITHUB_YAML),
            GITLAB: Source(GITLAB, GITLAB_YAML),
            BITBUCKET: Source(BITBUCKET, BITBUCKET_YAML)
        }

    def add_source(self, source: Optional[Source]):
        """Returns all project names containing forks

        :param Optional[Source] source: Source to add
        """

        if source is None:
            return

        self._source_names.add(source.name)

        if source.is_reference():
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

    def validate_sources(self) -> bool:
        """Validate sources

        :return: Source with supplied name
        :rtype: Source
        """

        if name not in self._sources:
            # TODO: Rename error to SOURCE_NOT_DEFINED
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, "No source defined")

        return self._sources[name]


SOURCE_CONTROLLER: SourceController = SourceController()
