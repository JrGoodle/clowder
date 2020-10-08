# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from typing import Dict, Optional

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

from .model.git_settings import GitSettings, GitConfig


class ResolvedGitSettings:
    """clowder yaml GitSettings model class

    :ivar bool submodules: Whether to fetch submodules
    :ivar bool recursive: Whether to fetch submodules recursively
    :ivar bool lfs: Whether to set up lfs hooks and pull files
    :ivar bool depth: Depth to clone git repositories
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self):
        """Source __init__"""

        self.submodules: bool = False
        self.recursive: bool = False
        self.lfs: bool = False
        self.depth: int = 0
        self.config: Optional[GitConfig] = None

    def update(self, git_settings: GitSettings) -> None:
        """Update with overrides from given GitSettings

        :return: Config processed to create strings
        :rtype: dict
        """

        if git_settings.submodules is not None:
            submodules = copy.deepcopy(git_settings.submodules)
            if isinstance(submodules, bool):
                self.submodules = submodules
                self.recursive = False
            elif isinstance(submodules, str):
                if submodules == "recursive":
                    self.submodules = True
                    self.recursive = True
                else:
                    err = ClowderError(ClowderErrorType.WRONG_SUBMODULES_TYPE, fmt.error_wrong_submodules_type())
                    LOG_DEBUG("Wrong submodules type", err)
                    raise err
            else:
                err = ClowderError(ClowderErrorType.WRONG_SUBMODULES_TYPE, fmt.error_wrong_submodules_type())
                LOG_DEBUG("Wrong submodules type", err)
                raise err
        if git_settings.lfs is not None:
            self.lfs = copy.deepcopy(git_settings.lfs)
        if git_settings.depth is not None:
            self.depth = copy.deepcopy(git_settings.depth)
        if git_settings.config is not None:
            if self.config is None:
                self.config = copy.deepcopy(git_settings.config)
            else:
                for (k, v) in git_settings.config.items():
                    self.config[k] = v

        self._clean_config()

    def _clean_config(self) -> None:
        """Remove any null value entries from config"""

        if self.config is None:
            return

        new_config = copy.deepcopy(self.config)
        for (k, v) in self.config.items():
            if v is None:
                del new_config[k]
        self.config = new_config

    def get_processed_config(self) -> Optional[Dict[str, str]]:
        """Return version of config converted to strings

        :return: Config processed to create strings
        :rtype: Optional[Dict[str, str]]
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
