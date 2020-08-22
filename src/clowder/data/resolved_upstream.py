# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from termcolor import colored

from clowder.environment import ENVIRONMENT
from clowder.git import ProjectRepo
from clowder.git.util import (
    existing_git_repository,
    git_url
)

from .model import Defaults, Group, Source, Upstream
from .source_controller import SOURCE_CONTROLLER, GITHUB


class ResolvedUpstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar Source source: Upstream source
    :ivar str remote: Upstream remote name
    :ivar str ref: Upstream git ref

    :ivar str path: Project relative path
    """

    def __init__(self, path: Path, upstream: Upstream, defaults: Optional[Defaults], group: Optional[Group]):
        """Upstream __init__

        :param Path path: Parent project path
        :param Upstream upstream: Upstream model instance
        :param Optional[Defaults] defaults: Defaults model instance
        :param Optional[Group] group: Group model instance
        """

        has_defaults = defaults is not None
        has_group = group is not None
        has_group_defaults = has_group and group.defaults is not None

        self.path: Path = path
        self.name: str = upstream.name

        has_remote = upstream.remote is not None
        has_defaults_remote = has_defaults and defaults.remote is not None
        has_group_defaults_remote = has_group_defaults and group.defaults.remote is not None
        self.remote: str = "upstream"
        if has_remote:
            self.remote = upstream.remote
        elif has_group_defaults_remote:
            self.remote = group.defaults.remote
        elif has_defaults_remote:
            self.remote = defaults.remote

        has_source = upstream.source is not None
        has_defaults_source = has_defaults and defaults.source is not None
        has_group_defaults_source = has_group_defaults and group.defaults.source is not None
        self.source: Source = SOURCE_CONTROLLER.get_source(GITHUB)
        if has_source:
            self.source = SOURCE_CONTROLLER.get_source(upstream.source.name)
        elif has_group_defaults_source:
            self.source = SOURCE_CONTROLLER.get_source(group.defaults.source)
        elif has_defaults_source:
            self.source = SOURCE_CONTROLLER.get_source(defaults.source)
        SOURCE_CONTROLLER.add_source(self.source)

        has_ref = upstream.get_formatted_ref() is not None
        has_defaults_ref = has_defaults and defaults.get_formatted_ref() is not None
        has_group_defaults_ref = has_group_defaults and group.defaults.get_formatted_ref() is not None
        self.ref: str = "refs/heads/master"
        if has_ref:
            self.ref = upstream.get_formatted_ref()
        elif has_group_defaults_ref:
            self.ref = group.defaults.get_formatted_ref()
        elif has_defaults_ref:
            self.ref = defaults.get_formatted_ref()

    def full_path(self) -> Path:
        """Return full path to project

        :return: Project's full file path
        :rtype: Path
        """

        return ENVIRONMENT.clowder_dir / self.path

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

        return git_url(self.source.protocol, self.source.url, self.name)
