# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from typing import Dict, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

GitConfig = Dict[str, Union[bool, str, int, float, None]]
GitSubmodules = Union[bool, str] # TODO: Replace str with enum for "update", "recursive", "update recursive"


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
    :ivar Optional[int] jobs: Number of jobs to use forr git clone and fetch
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self, yaml: dict):
        """Source __init__

        :param dict yaml: Parsed YAML python object for GitSettings
        """

        self.submodules: Optional[GitSubmodules] = yaml.get('recursive', None)
        self.lfs: Optional[bool] = yaml.get('lfs', None)
        self.depth: Optional[int] = yaml.get('depth', None)
        self.jobs: Optional[int] = yaml.get('jobs', None)
        self.config: Optional[GitConfig] = yaml.get('config', None)

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

        git_settings = {}

        if self._recursive is not None:
            git_settings['recursive'] = self._recursive
        if self._lfs is not None:
            git_settings['lfs'] = self._lfs
        if self._depth is not None:
            git_settings['depth'] = self._depth
        if self._jobs is not None:
            git_settings['jobs'] = self._jobs
        if self._config is not None:
            git_settings['config'] = self._config

        return git_settings

    @staticmethod
    def _combine_configs(current_config: Optional[GitConfig],
                         ancestor_config: Optional[GitConfig]) -> Optional[GitConfig]:
        """Combine project git config with default git config

        :param Optional[GitConfig] current_config: Current git config
        :param Optional[GitConfig] ancestor_config: Ancestor config to combine with
        :return: Combined git config
        :rtype: Optional[GitConfig]
        """

        if current_config is None and ancestor_config is None:
            return None

        if ancestor_config is None:
            return current_config

        if current_config is None:
            return ancestor_config

        config = copy.deepcopy(ancestor_config)
        for key, value in current_config.items():
            if key in config and value is None:
                del config[key]
                continue
            config[key] = value

        return config
