# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional, Union

from clowder.git.util import (
    format_git_branch,
    format_git_tag
)

from .source import Source


class Upstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar Optional[Source] source: Upstream source
    :ivar Optional[str] remote: Upstream remote name
    :ivar str ref: Upstream git ref

    :ivar str path: Project relative path
    """

    def __init__(self, yaml: Union[str, dict]):
        """Upstream __init__

        :param dict yaml: Parsed YAML python object for upstream
        """

        self.name: str = yaml['name']
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)
        self.remote: Optional[str] = yaml.get('remote', None)

        source = yaml.get('source', None)
        self.source: Optional[Source] = Source(source) if source is not None else None

    def get_formatted_ref(self) -> Optional[str]:
        """Return formatted git ref

        :return: Formatted git ref
        :rtype: str
        """

        if self.branch is not None:
            return format_git_branch(self.branch)
        elif self.tag is not None:
            return format_git_tag(self.tag)
        elif self.commit is not None:
            return self.commit
        else:
            return None

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

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
