# -*- coding: utf-8 -*-
"""Config handler class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Tuple

import clowder.util.formatting as fmt
from clowder import CLOWDER_DIR, CLOWDER_CONFIG_DIR, CLOWDER_CONFIG_YAML
from clowder.error import ClowderConfigYAMLError, ClowderConfigYAMLErrorType, ClowderExit
from clowder.util.file_system import (
    create_backup_file,
    make_dir,
    remove_file,
    restore_from_backup_file
)
from clowder.util.yaml import (
    load_clowder_config_yaml,
    save_yaml,
    validate_clowder_config_yaml
)

from .clowder_config import ClowderConfig

CONFIG_VERSION = 0.1


class Config(object):
    """Config handler class

    :ivar float version: Version number of config file
    :ivar Tuple[ClowderConfig, ...] clowder_configs: Configs for clowders
    :ivar Optional[ClowderConfig] current_clowder_config: Config for current clowder
    :ivar Optional[Exception] error: Exception from failing to load clowder config yaml file
    """

    def __init__(self, current_clowder_name: Optional[str], project_options: Tuple[str, ...]):
        """Config __init__"""

        self.error = None
        self.current_clowder_config = None
        self.clowder_configs = ()
        self._project_options = project_options

        # Config file doesn't currently exist
        if not CLOWDER_CONFIG_YAML.is_file():
            self.version = CONFIG_VERSION
            current_clowder_config = ClowderConfig(current_clowder_name=current_clowder_name,
                                                   project_options=self._project_options)
            self.clowder_configs = (current_clowder_config,)
            self.current_clowder_config = current_clowder_config
            return

        # Config file does exist, try to load
        self._load_clowder_config_yaml()

        # If current clowder exists, return
        if self.current_clowder_config is not None:
            return

        # If current clowder config doesn't exist, create empty one
        self.current_clowder_config = ClowderConfig(current_clowder_name=current_clowder_name,
                                                    project_options=self._project_options)
        if not self.clowder_configs:
            self.clowder_configs = (self.current_clowder_config,)
        else:
            configs = list(self.clowder_configs)
            configs.append(self.current_clowder_config)
            self.clowder_configs = tuple(configs)

    def process_projects_arg(self, projects: List[str]) -> Tuple[str, ...]:
        """Process project args based on parameters and config

        :param List[str] projects: Projects to filter
        :return: Projects in groups matching given names
        :rtype: Tuple[str, ...]
        """

        if projects != ['default']:
            return tuple(sorted(projects))

        if self.current_clowder_config.projects is None:
            return ('all',)

        return self.current_clowder_config.projects

    def save(self) -> None:
        """Save configuration to file"""

        # If directory doesn't exist, create it
        make_dir(CLOWDER_CONFIG_DIR)

        # If file doesn't exist, save it
        if not CLOWDER_CONFIG_YAML.is_file():
            save_yaml(self._get_yaml(), CLOWDER_CONFIG_YAML)
            return

        # If file does exist, move to .backup
        create_backup_file(CLOWDER_CONFIG_YAML)

        try:
            # Save new file
            remove_file(CLOWDER_CONFIG_YAML)
            save_yaml(self._get_yaml(), CLOWDER_CONFIG_YAML)
        except: # noqa
            # If failed, restore backup
            restore_from_backup_file(CLOWDER_CONFIG_YAML)

    def validate(self) -> None:
        """Check that config was created successfully"""

        if self.error is not None:
            print(f"{fmt.ERROR} Clowder config file appears to be invalid")
            raise ClowderExit(self.error.code)

    def _get_yaml(self) -> dict:
        """Get yaml representation of config

        :return: YAML python object
        :rtype: dict
        """

        clowder_configs = [c.get_yaml() for c in self.clowder_configs if not c.is_empty()]
        config = {'version': self.version, 'clowder_configs': clowder_configs}
        return config

    def _load_clowder_config_yaml(self) -> None:
        """Load clowder config yaml file

        :raise ClowderExit:
        """

        try:
            parsed_yaml = load_clowder_config_yaml()
            validate_clowder_config_yaml(parsed_yaml)

            self.version = parsed_yaml['version']

            configs = parsed_yaml['clowder_configs']
            clowder_configs = []
            for config in configs:
                clowder_configs.append(ClowderConfig(clowder_config=config,
                                                     project_options=self._project_options))
            self.clowder_configs = tuple(clowder_configs)

            if CLOWDER_DIR is not None:
                for config in self.clowder_configs:
                    if config.clowder_dir.resolve() == CLOWDER_DIR.resolve():
                        self.current_clowder_config = config
                        break
        except (AttributeError, KeyError, TypeError):
            self.version = CONFIG_VERSION
            self.clowder_configs = ()
            self.current_clowder_config = None
            raise ClowderConfigYAMLError(f"{fmt.ERROR} Invalid config yaml file", ClowderConfigYAMLErrorType.UNKNOWN)
        except (KeyboardInterrupt, SystemExit):
            raise ClowderExit(1)
