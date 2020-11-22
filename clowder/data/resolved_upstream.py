"""Representation of clowder yaml upstream

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from clowder.environment import ENVIRONMENT
from clowder.git import GitProtocol, GitRef, ProjectRepo
from clowder.git.util import existing_git_repository
import clowder.util.formatting as fmt

from .model import Defaults, Group, Source, Upstream
from .source_controller import SOURCE_CONTROLLER, GITHUB


class ResolvedUpstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar str path: Project relative path
    :ivar Source source: Upstream source
    :ivar str remote: Upstream remote name
    :ivar str ref: Upstream git ref
    :ivar Optional[GitProtocol] default_protocol: Default git protocol to use
    """

    def __init__(self, path: Path, upstream: Upstream, defaults: Optional[Defaults],
                 group: Optional[Group], protocol: Optional[GitProtocol]):
        """Upstream __init__

        :param Path path: Parent project path
        :param Upstream upstream: Upstream model instance
        :param Optional[Defaults] defaults: Defaults model instance
        :param Optional[Group] group: Group model instance
        :param Optional[GitProtocol] protocol: Git protocol
        """

        self._repo: Optional[ProjectRepo] = None

        has_defaults = defaults is not None
        has_upstream_defaults = has_defaults and defaults.upstream_defaults is not None
        has_group = group is not None
        has_group_defaults = has_group and group.defaults is not None
        has_group_upstream_defaults = has_group_defaults and group.defaults.upstream_defaults is not None

        self.path: Path = path
        self.name: str = upstream.name
        self.ref: Optional[GitRef] = None

        has_remote = upstream.remote is not None
        has_defaults_remote = has_upstream_defaults and defaults.upstream_defaults.remote is not None
        has_group_defaults_remote = has_group_upstream_defaults and group.defaults.upstream_defaults.remote is not None
        self.remote: str = "upstream"
        if has_remote:
            self.remote: str = upstream.remote
        elif has_group_defaults_remote:
            self.remote: str = group.defaults.upstream_defaults.remote
        elif has_defaults_remote:
            self.remote: str = defaults.upstream_defaults.remote

        has_source = upstream.source is not None
        has_defaults_source = has_upstream_defaults and defaults.upstream_defaults.source is not None
        has_group_defaults_source = has_group_upstream_defaults and group.defaults.upstream_defaults.source is not None
        self.source: Source = SOURCE_CONTROLLER.get_source(GITHUB)
        if has_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(upstream.source)
        elif has_group_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(group.defaults.upstream_defaults.source)
        elif has_defaults_source:
            self.source: Source = SOURCE_CONTROLLER.get_source(defaults.upstream_defaults.source)

        self.default_protocol: Optional[GitProtocol] = None
        if self.source.protocol is not None:
            self.default_protocol: Optional[GitProtocol] = self.source.protocol
        elif protocol is not None:
            self.default_protocol: Optional[GitProtocol] = protocol

    @property
    def full_path(self) -> Path:
        """Full path to project"""

        return ENVIRONMENT.clowder_dir / self.path

    @property
    def repo(self) -> ProjectRepo:
        """ProjectRepo instance"""

        if self._repo is not None:
            return self._repo

        self._repo = ProjectRepo(self.full_path, self.remote, self.ref)
        return self._repo

    def status(self) -> str:
        """Return formatted upstream status

        :return: Formatted upstream status
        """

        if not existing_git_repository(self.path):
            return fmt.green(self.path)

        repo = ProjectRepo(self.full_path, self.remote, self.ref)
        project_output = repo.format_project_string(self.path)
        return f"{project_output} {repo.formatted_ref}"

    def update_default_branch(self, branch: str) -> None:
        """Update ref with default branch if none set"""

        if self.ref is None:
            self.ref = GitRef(branch=branch)

    @property
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

        return protocol.format_url(self.source.url, self.name)
