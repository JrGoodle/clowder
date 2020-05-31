# -*- coding: utf-8 -*-
"""Representation of clowder yaml fork

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

from .defaults import Defaults
from .source import Source

if TYPE_CHECKING:
    from .project import Project


class ForkImpl(object):
    """clowder yaml Fork model impl class

    :ivar str name: Project name
    """

    def __init__(self, fork: dict):
        """ForkImpl __init__

        :param dict fork: Parsed YAML python object for fork
        """

        self.name: str = fork['name']
        self._remote: Optional[str] = fork.get('remote', None)
        self._branch: Optional[str] = fork.get("branch", None)
        self._tag: Optional[str] = fork.get("tag", None)
        self._commit: Optional[str] = fork.get("commit", None)
        self._source: Optional[str] = fork.get('source', None)

    def get_yaml(self, resolved_sha: Optional[str] = None) -> dict:
        """Return python object representation for saving yaml

        :param Optional[str] resolved_sha: Current commit sha
        :return: YAML python object
        :rtype: dict
        """

        fork = {'name': self.name}

        if self._remote is not None:
            fork['remote'] = self._remote
        if self._source is not None:
            fork['source'] = self._source

        if resolved_sha is None:
            if self._branch is not None:
                fork['branch'] = self._branch
            elif self._tag is not None:
                fork['tag'] = self._tag
            elif self._commit is not None:
                fork['commit'] = self._commit
        else:
            fork['commit'] = resolved_sha

        return fork


class Fork(ForkImpl):
    """clowder yaml Fork model class

    :ivar str path: Project relative path
    :ivar str remote: Fork remote name
    :ivar str ref: Fork git ref
    """

    def __init__(self, fork: dict, project: 'Project', sources: Tuple[Source, ...], defaults: Defaults):
        """Fork __init__

        :param dict fork: Parsed YAML python object for fork
        :param Project project: Parent project
        :param Tuple[Source, ...] sources: List of Source instances
        :param Defaults defaults: Defaults instance
        """

        super().__init__(fork)

        self.path = project.path
        self.recursive = project.git_settings.recursive
        self.remote = fork.get('remote', defaults.remote)

        if self._branch is not None:
            self.ref = format_git_branch(self._branch)
        elif self._tag is not None:
            self.ref = format_git_tag(self._tag)
        elif self._commit is not None:
            self.ref = self._commit
        else:
            self.ref = defaults.ref

        self.source = None
        source_name = fork.get('source', defaults.source)
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

    def status(self) -> str:
        """Return formatted fork status

        :return: Formatted fork status
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
