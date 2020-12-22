"""Representation of clowder yaml upstream

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Any, Optional

from pygoodle.git import Protocol, Remote

from clowder.environment import ENVIRONMENT

from .model import Defaults, Section, Source, Upstream
from .source_controller import SOURCE_CONTROLLER, GITHUB


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

        :param Path path: Parent project path
        :param Upstream upstream: Upstream model instance
        :param Optional[Defaults] defaults: Defaults model instance
        :param Optional[Section] section: Section model instance
        :param Optional[Protocol] protocol: Git protocol
        """

        self.path: Path = path
        self.name: str = upstream.name
        remote = self._get_property('remote', upstream, defaults, section, default='upstream')
        self.remote: Remote = Remote(self.full_path, remote)

        source = self._get_property('source', upstream, defaults, section, default=GITHUB)
        self.source: Source = SOURCE_CONTROLLER.get_source(source)

        self.default_protocol: Optional[Protocol] = None
        if self.source.protocol is not None:
            self.default_protocol: Optional[Protocol] = self.source.protocol
        elif protocol is not None:
            self.default_protocol: Optional[Protocol] = protocol

    @property
    def full_path(self) -> Path:
        """Full path to project"""

        return ENVIRONMENT.clowder_dir / self.path

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
                      default: Optional[Any] = None) -> Optional[Any]:
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
