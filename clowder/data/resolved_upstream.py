# -*- coding: utf-8 -*-
"""Representation of clowder yaml upstream

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from termcolor import colored

from clowder.environment import ENVIRONMENT
from clowder.git_project import ProjectRepo
from clowder.git_project.util import (
    existing_git_repository,
    git_url
)

from .model import Defaults, Group, Source, Upstream
from .source_controller import SOURCE_CONTROLLER, GITHUB


class ResolvedUpstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar str path: Project relative path
    :ivar Source source: Upstream source
    :ivar str remote: Upstream remote name
    :ivar str ref: Upstream git ref
    :ivar Optional[str] default_protocol: Default git protocol to use
    """

    def __init__(self, path: Path, upstream: Upstream, defaults: Optional[Defaults],
                 group: Optional[Group], protocol: Optional[str]):
        """Upstream __init__

        :param Path path: Parent project path
        :param Upstream upstream: Upstream model instance
        :param Optional[Defaults] defaults: Defaults model instance
        :param Optional[Group] group: Group model instance
        """

        has_defaults = defaults is not None
        has_upstream_defaults = has_defaults and defaults.upstream_defaults is not None
        has_group = group is not None
        has_group_defaults = has_group and group.defaults is not None
        has_group_upstream_defaults = has_group_defaults and group.defaults.upstream_defaults is not None

        self.path: Path = path
        self.name: str = upstream.name
        # TODO: Remove dependence on hardcoded branch. Defer to origin/HEAD
        self.ref: str = "refs/heads/master"

        has_remote = upstream.remote is not None
        has_defaults_remote = has_upstream_defaults and defaults.upstream_defaults.remote is not None
        has_group_defaults_remote = has_group_upstream_defaults and group.defaults.upstream_defaults.remote is not None
        self.remote: str = "upstream"
        if has_remote:
            self.remote = upstream.remote
        elif has_group_defaults_remote:
            self.remote = group.defaults.upstream_defaults.remote
        elif has_defaults_remote:
            self.remote = defaults.upstream_defaults.remote

        has_source = upstream.source is not None
        has_defaults_source = has_upstream_defaults and defaults.upstream_defaults.source is not None
        has_group_defaults_source = has_group_upstream_defaults and group.defaults.upstream_defaults.source is not None
        if has_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(upstream.source)
        elif has_group_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(group.defaults.upstream_defaults.source)
        elif has_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(defaults.upstream_defaults.source)
        else:
            self.source: Source = SOURCE_CONTROLLER.get_source(GITHUB)

        has_group_protocol = has_group and group.protocol is not None
        if self.source.protocol is not None:
            self.default_protocol: Optional[str] = self.source.protocol
        elif has_group_protocol:
            self.default_protocol: Optional[str] = group.protocol
        elif protocol is not None:
            self.default_protocol: Optional[str] = protocol
        else:
            self.default_protocol: Optional[str] = None

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

        if self.source.protocol is not None:
            protocol = self.source.protocol
        elif SOURCE_CONTROLLER.protocol_override is not None:
            protocol = SOURCE_CONTROLLER.protocol_override
        elif self.default_protocol is not None:
            protocol = self.default_protocol
        else:
            protocol = SOURCE_CONTROLLER.get_default_protocol()

        return git_url(protocol, self.source.url, self.name)
