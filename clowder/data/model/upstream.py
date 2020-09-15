# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

from .source import Source
from .source_name import SourceName


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

    def get_yaml(self) -> Union[str, dict]:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: Union[str, dict]
        """

        if self._is_string:
            return self.name

        yaml = {"name": self.name}

        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source.get_yaml()

        return yaml
