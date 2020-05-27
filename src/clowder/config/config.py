# -*- coding: utf-8 -*-
"""Config handler class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import List, Optional, Tuple

import clowder.util.formatting as fmt
from clowder import CLOWDER_DIR, CLOWDER_CONFIG_DIR, CLOWDER_CONFIG_YAML, LOG_DEBUG
from clowder.error import ClowderError, ClowderErrorType
from clowder.util.file_system import (
    create_backup_file,
    make_dir,
    remove_file,
    restore_from_backup_file
)
from clowder.util.yaml import (
    load_yaml_file,
    save_yaml_file,
    validate_yaml_file
)

from .clowder_config import ClowderConfig

CONFIG_VERSION = '0.1'


class Config(object):
    """Config handler class

    :ivar float version: Version number of config file
    :ivar Tuple[ClowderConfig, ...] clowder_configs: Configs for clowders
    :ivar Optional[ClowderConfig] current_clowder_config: Config for current clowder
    :ivar Optional[Exception] error: Exception from failing to load clowder config yaml file
    """

    def __init__(self, current_clowder_name: Optional[str], project_options: Tuple[str, ...]):
        """Config __init__"""

        self.error: Optional[Exception] = None
        self.current_clowder_config: Optional[ClowderConfig] = None
        self.clowder_configs: Tuple[ClowderConfig, ...] = ()
        self._project_options = project_options

        # Config file doesn't currently exist
        if not CLOWDER_CONFIG_YAML.is_file():
            self.version = CONFIG_VERSION
            current_clowder_config = ClowderConfig(current_clowder_name=current_clowder_name)
            self.clowder_configs = (current_clowder_config,)
            self.current_clowder_config = current_clowder_config
            return

        # Config file does exist, try to load
        self._load_clowder_config_yaml()

        # If current clowder exists, return
        if self.current_clowder_config is not None:
            return

        # If current clowder config doesn't exist, create empty one
        self.current_clowder_config = ClowderConfig(current_clowder_name=current_clowder_name)
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
            save_yaml_file(self._get_yaml(), CLOWDER_CONFIG_YAML)
            return

        # If file does exist, move to .backup
        create_backup_file(CLOWDER_CONFIG_YAML)

        try:
            # Save new file
            remove_file(CLOWDER_CONFIG_YAML)
            save_yaml_file(self._get_yaml(), CLOWDER_CONFIG_YAML)
        except ClowderError as err:
            LOG_DEBUG('Failed to save configuration file', err)
            # If failed, restore backup
            # TODO: Handle possible exception
            restore_from_backup_file(CLOWDER_CONFIG_YAML)
            raise
        except Exception as err:
            LOG_DEBUG('Failed to save configuration file', err)
            # If failed, restore backup
            # TODO: Handle possible exception
            restore_from_backup_file(CLOWDER_CONFIG_YAML)
            raise

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

        :raise ClowderError:
        """

        try:
            parsed_yaml = load_yaml_file(CLOWDER_CONFIG_YAML, CLOWDER_CONFIG_DIR)
            validate_yaml_file(parsed_yaml, CLOWDER_CONFIG_YAML)

            self.version = parsed_yaml['version']

            configs = parsed_yaml['clowder_configs']
            clowder_configs = []
            for config in configs:
                clowder_configs.append(ClowderConfig(clowder_config=config))
            self.clowder_configs = tuple(clowder_configs)

            if CLOWDER_DIR is not None:
                for config in self.clowder_configs:
                    if config.clowder_dir.resolve() == CLOWDER_DIR.resolve():
                        self.current_clowder_config = config
                        self.current_clowder_config.validate_config_projects_defined(self._project_options)
                        break
        except (AttributeError, KeyError, TypeError) as err:
            self.version = CONFIG_VERSION
            self.clowder_configs = ()
            self.current_clowder_config = None
            LOG_DEBUG('Failed to load clowder config', err)
            raise ClowderError(ClowderErrorType.CONFIG_YAML_UNKNOWN, fmt.error_invalid_config_file(CLOWDER_CONFIG_YAML))
        except (KeyboardInterrupt, SystemExit):
            raise ClowderError(ClowderErrorType.USER_INTERRUPT, fmt.error_user_interrupt())
