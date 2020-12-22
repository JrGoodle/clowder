"""Representation of clowder yaml upstream

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional, TypeVar

from pygoodle.git import Protocol, Remote

from clowder.environment import ENVIRONMENT
from clowder.model import Defaults, Section, Source, Upstream
from clowder.controller import SOURCE_CONTROLLER, GITHUB

T = TypeVar('T')


class ResolvedUpstream:
    """clowder yaml Upstream model class

    :ivar str name: Upstream name
    :ivar str path: Project relative path
    :ivar Source source: Upstream source
    :ivar str remote: Upstream remote name
    :ivar str ref: Upstream git ref
    :ivar Optional[Protocol] protocol: Default git protocol to use
    """

    def __init__(self, path: Path, upstream: Upstream, defaults: Optional[Defaults],
                 section: Optional[Section], protocol: Optional[Protocol]):
        """Upstream __init__

        :param Path path: Parent project relative path
        :param Upstream upstream: Upstream model instance
        :param Optional[Defaults] defaults: Defaults model instance
        :param Optional[Section] section: Section model instance
        :param Optional[Protocol] protocol: Git protocol
        """

        self.relative_path: Path = path
        self.path: Path = ENVIRONMENT.clowder_dir / self.relative_path
        self.name: str = upstream.name
        remote = self._get_property('remote', upstream, defaults, section, default='upstream')
        self.remote: Remote = Remote(self.path, remote)

        source = self._get_property('source', upstream, defaults, section, default=GITHUB)
        self.source: Source = SOURCE_CONTROLLER.get_source(source)

        self.default_protocol: Optional[Protocol] = None
        if self.source.protocol is not None:
            self.default_protocol: Optional[Protocol] = self.source.protocol
        elif protocol is not None:
            self.default_protocol: Optional[Protocol] = protocol

    def __lt__(self, other: 'ResolvedUpstream') -> bool:
        return self.name.lower() < self.name.lower()

    def __eq__(self, other) -> bool:
        if not isinstance(other, ResolvedUpstream):
            return False
        return self.name == other.name and self.path == other.path

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

    @staticmethod
    def _get_property(name: str, upstream: Upstream, defaults: Optional[Defaults], section: Optional[Section],
                      default: Optional[T] = None) -> Optional[T]:
        upstream_value = getattr(upstream, name)
        has_defaults = defaults is not None
        has_upstream_defaults = has_defaults and defaults.upstream_defaults is not None
        defaults_value = getattr(defaults.upstream_defaults, name) if has_upstream_defaults else None
        has_section = section is not None
        has_section_defaults = has_section and section.defaults is not None
        has_section_upstream_defaults = has_section_defaults and section.defaults.upstream_defaults is not None
        section_defaults_value = getattr(section.defaults.upstream_defaults, name) if has_section_upstream_defaults else None  # noqa
        if upstream_value is not None:
            return upstream_value
        elif section_defaults_value is not None:
            return section_defaults_value
        elif defaults_value is not None:
            return defaults_value
        elif default is not None:
            return default
        else:
            return None
