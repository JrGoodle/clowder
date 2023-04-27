"""Representation of clowder yaml defaults

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import Optional

from .git_settings import GitSettings
from .source import SourceName
from .upstream_defaults import UpstreamDefaults


class Defaults:
    """clowder yaml Defaults model class

    :ivar Optional[SourceName] source: Default source name
    :ivar Optional[str] remote: Default remote name
    :ivar Optional[GitSettings] git_settings: Custom git settings
    :ivar Optional[str] branch: Default git branch
    :ivar Optional[str] tag: Default git tag
    :ivar Optional[str] commit: Default commit sha-1
    :ivar Optional[UpstreamDefaults] upstream_defaults: Upstream defaults
    """

    def __init__(self, yaml: dict):
        """Defaults __init__

        :param dict yaml: Parsed YAML python object for defaults
        """

        source = yaml.get("source", None)
        self.source: Optional[SourceName] = None if source is None else SourceName(source)
        self.remote: Optional[str] = yaml.get("remote", None)
        git = yaml.get("git", None)
        self.git_settings: Optional[GitSettings] = None if git is None else GitSettings(git)
        self.branch: Optional[str] = yaml.get("branch", None)
        self.tag: Optional[str] = yaml.get("tag", None)
        self.commit: Optional[str] = yaml.get("commit", None)
        upstream = yaml.get("upstream", None)
        upstream_defaults = None if upstream is None else UpstreamDefaults(upstream)
        self.upstream_defaults: Optional[UpstreamDefaults] = upstream_defaults

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        """

        yaml = {}

        if self.branch is not None:
            yaml['branch'] = self.branch
        elif self.tag is not None:
            yaml['tag'] = self.tag
        elif self.commit is not None:
            yaml['commit'] = self.commit

        if self.remote is not None:
            yaml['remote'] = self.remote
        if self.source is not None:
            yaml['source'] = self.source
        if self.git_settings is not None:
            yaml['git'] = self.git_settings.get_yaml()
        if self.upstream_defaults is not None:
            yaml['upstream'] = self.upstream_defaults.get_yaml()

        return yaml
