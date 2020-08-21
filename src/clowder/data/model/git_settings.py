# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

GitConfig = Dict[str, Union[bool, str, int, float, None]]
GitSubmodules = Union[bool, str]  # TODO: Replace str with enum for "update", "recursive", "update recursive"


class DefaultGitSettings:
    """Default GitSettings class

    :cvar bool recursive: Default for whether to run git commands recursively
    :cvar bool lfs: Default for whether to set up lfs hooks and pull files
    :cvar int depth: Default depth to clone git repositories
    :cvar int jobs: Default number of jobs to use forr git clone and fetch
    """

    recursive = False
    lfs = False
    depth = 0
    jobs = 1


class GitSettings:
    """clowder yaml GitSettings model class

    :ivar Optional[bool] submodules: Whether to fetch submodules
    :ivar Optional[bool] lfs: Whether to set up lfs hooks and pull files
    :ivar Optional[bool] depth: Depth to clone git repositories
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self, yaml: dict):
        """Source __init__

        :param dict yaml: Parsed YAML python object for GitSettings
        """

        self.submodules: Optional[GitSubmodules] = yaml.get('recursive', None)
        self.lfs: Optional[bool] = yaml.get('lfs', None)
        self.depth: Optional[int] = yaml.get('depth', None)
        self.config: Optional[GitConfig] = yaml.get('config', None)

    @staticmethod
    def combine(high_priority_git_settings: 'GitSettings',
                low_priority_git_settings: 'GitSettings') -> 'GitSettings':
        """Return new combined git settings

        :return: Config processed to create strings
        :rtype: dict
        """

        combined = GitSettings({})

        combined.submodules = low_priority_git_settings.submodules
        combined.lfs = low_priority_git_settings.lfs
        combined.depth = low_priority_git_settings.depth
        combined.config = low_priority_git_settings.config

        if high_priority_git_settings.submodules is not None:
            combined.submodules = high_priority_git_settings.submodules
        if high_priority_git_settings.lfs is not None:
            combined.lfs = high_priority_git_settings.lfs
        if high_priority_git_settings.depth is not None:
            combined.depth = high_priority_git_settings.depth
        if high_priority_git_settings.config is not None:
            # TODO: Properly combine config dicts
            combined.config = high_priority_git_settings.config

        return combined

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
