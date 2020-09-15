# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.git.util import (
    format_git_branch,
    format_git_tag
)
from clowder.logging import LOG_DEBUG

from .source import Source
from .source_name import SourceName


class Upstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar str path: Project relative path
    :ivar Optional[Union[Source, SourceName]] source: Upstream source
    :ivar Optional[str] remote: Upstream remote name
    :ivar Optional[str] branch: Git branch
    :ivar Optional[str] tag: Git tag
    :ivar Optional[str] commit: Git commit
    """

    def __init__(self, yaml: Union[str, dict]):
        """Upstream __init__

        :param Union[str, dict] yaml: Parsed YAML python object for upstream
        """

        self._is_string = False

        if isinstance(yaml, str):
            self._is_string = True
            self.name: str = yaml
            self.branch: Optional[str] = None
            self.tag: Optional[str] = None
            self.commit: Optional[str] = None
            self.remote: Optional[str] = None
            self.source: Optional[Union[Source, SourceName]] = None
            return

        if isinstance(yaml, dict):
            self.name: str = yaml['name']
            self.branch: Optional[str] = yaml.get("branch", None)
            self.tag: Optional[str] = yaml.get("tag", None)
            self.commit: Optional[str] = yaml.get("commit", None)
            self.remote: Optional[str] = yaml.get('remote', None)

            self.source: Optional[Union[Source, SourceName]] = None
            source = yaml.get('source', None)
            if source is not None:
                if isinstance(source, str):
                    self.source: Optional[Union[Source, SourceName]] = SourceName(source)
                elif isinstance(source, dict):
                    # Use upstream instance id as source name
                    name = SourceName(str(id(self)))
                    self.source: Optional[Union[Source, SourceName]] = Source(name, source)
                else:
                    err = ClowderError(ClowderErrorType.WRONG_SOURCE_TYPE, fmt.error_wrong_source_type())
                    LOG_DEBUG('Wrong source type', err)
                    raise err
            return

        err = ClowderError(ClowderErrorType.WRONG_UPSTREAM_TYPE, fmt.error_wrong_upstream_type())
        LOG_DEBUG('Wrong upstream type', err)
        raise err

    def get_formatted_ref(self) -> Optional[str]:
        """Return formatted git ref

        :return: Formatted git ref
        :rtype: Optional[str]
        """

        if self.branch is not None:
            return format_git_branch(self.branch)
        elif self.tag is not None:
            return format_git_tag(self.tag)
        elif self.commit is not None:
            return self.commit
        else:
            return None

    def get_yaml(self) -> Union[str, dict]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[str, dict]
        """

        if self._is_string:
            return self.name

        yaml = {"name": self.name}

        if self.branch is not None:
            yaml['branch'] = self.branch
        if self.tag is not None:
            yaml['tag'] = self.tag
        if self.commit is not None:
            yaml['commit'] = self.commit
        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source.get_yaml()

        return yaml
