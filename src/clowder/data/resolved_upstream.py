# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, Tuple, TYPE_CHECKING

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.git import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    format_git_branch,
    format_git_tag,
    git_url
)

from .model import Defaults, Source

if TYPE_CHECKING:
    from .model import Project


class ResolvedUpstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar Optional[Source] source: Upstream source
    :ivar Optional[str] remote: Upstream remote name
    :ivar str ref: Upstream git ref

    :ivar str path: Project relative path
    """

    def __init__(self, upstream: dict, project: 'Project', sources: Tuple[Source, ...], defaults: Defaults):
        """Upstream __init__

        :param dict upstream: Parsed YAML python object for upstream
        :param Project project: Parent project
        :param Tuple[Source, ...] sources: List of Source instances
        :param Defaults defaults: Defaults instance
        """

        self.name: str = upstream['name']
        self._remote: Optional[str] = upstream.get('remote', None)
        self._branch: Optional[str] = upstream.get("branch", None)
        self._tag: Optional[str] = upstream.get("tag", None)
        self._commit: Optional[str] = upstream.get("commit", None)
        self._source: Optional[str] = upstream.get('source', None)

        self.path = project.path
        self.recursive = project.git_settings.recursive
        self.remote = upstream.get('remote', 'upstream')

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self.ref = defaults.ref

        self.source = None
        source_name = upstream.get('source', defaults.source)
        for s in sources:
            if s.name == source_name:
                self.source = s
        if self.source is None:
            message = fmt.error_source_not_found(source_name, ENVIRONMENT.clowder_yaml, project.name, self.name)
            raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)

    def full_path(self) -> Path:
        """Return full path to project

        :return: Project's full file path
        :rtype: Path
        """

        return ENVIRONMENT.clowder_dir / self.path

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        upstream = {'name': self.name}

        if self._remote is not None:
            upstream['remote'] = self._remote
        if self._source is not None:
            upstream['source'] = self._source

        if resolved_sha is None:
            if self._branch is not None:
                upstream['branch'] = self._branch
            elif self._tag is not None:
                upstream['tag'] = self._tag
            elif self._commit is not None:
                upstream['commit'] = self._commit
        else:
            upstream['commit'] = resolved_sha

        return upstream

    def status(self) -> str:
        """Return formatted upstream status

        :return: Formatted upstream status
        :rtype: str
        """

        if not existing_git_repository(self.path):
            return colored(self.path, 'green')

        repo = ProjectRepo(self.full_path(), self.remote, self.ref)
        project_output = repo.format_project_string(self.path)
        current_ref_output = repo.format_project_ref_string()
        return f"{project_output} {current_ref_output}"

    def url(self) -> str:
        """Return project url"""

        return git_url(self.source.protocol.value, self.source.url, self.name)
