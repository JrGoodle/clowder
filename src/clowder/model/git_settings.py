# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from typing import Dict, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

GitConfig = Dict[str, Union[bool, str, int, float, None]]


class GitSettings:
    """clowder yaml GitSettings model class

    :cvar bool recursive: Default for whether to run git commands recursively
    :cvar bool lfs: Default for whether to set up lfs hooks and pull files
    :cvar int depth: Default depth to clone git repositories
    :cvar int jobs: Default number of jobs to use forr git clone and fetch

    :ivar Optional[bool] recursive: Whether to run git commands recursively
    :ivar Optional[bool] lfs: Whether to set up lfs hooks and pull files
    :ivar Optional[bool] depth: Depth to clone git repositories
    :ivar Optional[int] jobs: Number of jobs to use forr git clone and fetch
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    recursive = False
    lfs = False
    depth = 0
    jobs = 1

    def __init__(self, git_settings: Optional[dict] = None, parent_git_settings: Optional['GitSettings'] = None):
        """Source __init__

        :param Optional[dict] git_settings: Parsed YAML python object for GitSettings
        :param Optional[dict] parent_git_settings: Parsed YAML python object for default GitSettings
        """

        if git_settings is None and parent_git_settings is not None:
            raise ClowderError(ClowderErrorType.INVALID_GIT_SETTINGS_INIT_PARAMETERS,
                               'Invalid git settings init parameters')

        if git_settings is None:
            git_settings = {}

        self._recursive: Optional[bool] = git_settings.get('recursive', None)
        self._lfs: Optional[bool] = git_settings.get('lfs', None)
        self._depth: Optional[int] = git_settings.get('depth', None)
        self._jobs: Optional[int] = git_settings.get('jobs', None)
        self._config: Optional[GitConfig] = git_settings.get('config', None)

        if parent_git_settings is not None:
            self.recursive: bool = git_settings.get('recursive', parent_git_settings.recursive)
            self.lfs: bool = git_settings.get('lfs', parent_git_settings.lfs)
            self.depth: int = git_settings.get('depth', parent_git_settings.depth)
            self.jobs: int = git_settings.get('jobs', parent_git_settings.jobs)
            self.config: Optional[GitConfig] = self._combine_configs(git_settings.get('config', None),
                                                                     parent_git_settings.config)
        else:
            self.recursive: bool = git_settings.get('recursive', GitSettings.recursive)
            self.lfs: bool = git_settings.get('lfs', GitSettings.lfs)
            self.depth: int = git_settings.get('depth', GitSettings.depth)
            self.jobs: int = git_settings.get('jobs', GitSettings.jobs)
            self.config: Optional[GitConfig] = git_settings.get('config', None)

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
