# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from typing import Dict, Optional, Union

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType

GitConfig = Dict[str, Union[bool, str, int, float]]


class GitSettings(object):
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

    def __init__(self, yaml: dict, default_git_settings: Optional[dict] = None):
        """Source __init__

        :param dict yaml: Parsed YAML python object for GitSettings
        :param Optional[dict] default_git_settings: Parsed YAML python object for default GitSettings
        """

        self._recursive = yaml.get('recursive', None)
        self._lfs = yaml.get('lfs', None)
        self._depth = yaml.get('depth', None)
        self._jobs = yaml.get('jobs', None)
        self._config = yaml.get('config', None)

        if default_git_settings is not None:
            self.recursive = yaml.get('recursive', default_git_settings.get('recursive', None))
            self.lfs = yaml.get('lfs', default_git_settings.get('lfs', None))
            self.depth = yaml.get('depth', default_git_settings.get('depth', None))
            self.jobs = yaml.get('jobs', default_git_settings.get('jobs', None))
            # TODO: Combine configs, eliminating null entries
            self.config = yaml.get('config', default_git_settings.get('config', None))
        else:
            self.recursive = yaml.get('name', None)
            self.lfs = yaml.get('lfs', None)
            self.depth = yaml.get('depth', None)
            self.jobs = yaml.get('jobs', None)
            self.config = yaml.get('config', None)

    def get_processed_config(self) -> Optional[Dict[str, str]]:
        """Return version of config converted to strings

        :return: Config processed to create strings
        :rtype: dict
        """

        if self.config is None:
            return None

        config = {}
        for key, value in self.config:
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
