# -*- coding: utf-8 -*-
"""Representation of clowder yaml git settings

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict, Optional, Union

GitConfig = Dict[str, Union[bool, str, int, float, None]]
GitSubmodules = Union[bool, str]


class GitSettings:
    """clowder yaml GitSettings model class

    :ivar Optional[bool] submodules: Whether to fetch submodules
    :ivar Optional[bool] lfs: Whether to set up lfs hooks and pull files
    :ivar Optional[int] depth: Depth to clone git repositories
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self, yaml: dict):
        """Source __init__

        :param dict yaml: Parsed YAML python object for GitSettings
        """

        self.submodules: Optional[GitSubmodules] = yaml.get('submodules', None)
        self.lfs: Optional[bool] = yaml.get('lfs', None)
        self.depth: Optional[int] = yaml.get('depth', None)
        self.config: Optional[GitConfig] = yaml.get('config', None)

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
