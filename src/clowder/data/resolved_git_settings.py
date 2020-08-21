# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

from .model.git_settings import GitSettings, GitConfig, GitSubmodules


class ResolvedGitSettings:
    """clowder yaml GitSettings model class

    :ivar bool submodules: Whether to fetch submodules
    :ivar bool lfs: Whether to set up lfs hooks and pull files
    :ivar bool depth: Depth to clone git repositories
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self):
        """Source __init__"""

        self.submodules: GitSubmodules = False
        self.lfs: bool = False
        self.depth: int = 0
        self.config: Optional[GitConfig] = None

    def update(self, git_settings: GitSettings) -> None:
        """Update with overrides from given GitSettings

        :return: Config processed to create strings
        :rtype: dict
        """

        if git_settings.submodules is not None:
            self.submodules = git_settings.submodules
        if git_settings.lfs is not None:
            self.lfs = git_settings.lfs
        if git_settings.depth is not None:
            self.depth = git_settings.depth
        if git_settings.config is not None:
            if self.config is None:
                self.config = git_settings.config
            else:
                for (k, v) in git_settings.config:
                    self.config[k] = v

        self._clean_config()

    def _clean_config(self) -> None:
        """Remove any null value entries from config"""

        if self.config is None:
            return

        for (k, v) in self.config:
            if v is None:
                del self.config[k]

    def get_processed_config(self) -> Optional[Dict[str, str]]:
        """Return version of config converted to strings

        :return: Config processed to create strings
        :rtype: dict
        """

        if self.config is None:
            return None

        config: Dict[str, str] = {}
        for key, value in self.config.items():
            if isinstance(self.config[key], bool):
                config[key] = str(value).lower()
            elif isinstance(self.config[key], int) or isinstance(self.config[key], float):
                config[key] = str(value)
            elif isinstance(self.config[key], str):
                config[key] = value
            elif self.config[key] is None:
                pass
            else:
                raise ClowderError(ClowderErrorType.INVALID_GIT_CONFIG_VALUE,
                                   fmt.error_invalid_git_config_value(key, value))
        return config

    def get_yaml(self) -> dict:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        yaml = {}

        if self.submodules is not None:
            yaml['submodules'] = self.submodules
        if self.lfs is not None:
            yaml['lfs'] = self.lfs
        if self.depth is not None:
            yaml['depth'] = self.depth
        if self.config is not None:
            yaml['config'] = self.config

        return yaml
