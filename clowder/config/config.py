"""Config handler class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from typing import List, Optional, Tuple

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.util.error import MissingClowderRepoError
from clowder.util.file_system import (
    create_backup_file,
    make_dir,
    remove_file,
    restore_from_backup_file
)
from clowder.util.logging import LOG
from clowder.util.yaml import (
    load_yaml_file,
    save_yaml_file,
    validate_yaml_file
)

from .clowder_config import ClowderConfig

CONFIG_VERSION = 0.1


class Config(object):
    """Config handler class

    :ivar float version: Version number of config file
    :ivar Tuple[ClowderConfig, ...] clowder_configs: Configs for clowders
    :ivar Optional[ClowderConfig] current_clowder_config: Config for current clowder
    :ivar Optional[MissingClowderRepo] missing_clowder_repo_error: Missing clowder repo error
    :ivar Optional[Exception] load_clowder_config_error: Error from failing to load clowder config yaml file
    """

    def __init__(self, current_clowder_name: Optional[str],
                 project_options: Tuple[str, ...], raise_exceptions: bool = False):
        """Config __init__

        :param Optional[str] current_clowder_name: Name of currently loaded clowder if present
        :param Tuple[str, ...] project_options: Name of current clowder project options
        :param bool raise_exceptions: Whether to raise exception when from initializing invalid config file
        """

        self.load_clowder_config_error: Optional[Exception] = None
        self.missing_clowder_repo_error: Optional[MissingClowderRepoError] = None
        self.current_clowder_config: Optional[ClowderConfig] = None
        self.clowder_configs: Tuple[ClowderConfig, ...] = ()
        self._project_options: Tuple[str, ...] = project_options

        if ENVIRONMENT.clowder_repo_dir is None:
            err = MissingClowderRepoError("Failed to load clowder config file - .clowder directory doesn't exist")
            self.missing_clowder_repo_error: Optional[MissingClowderRepoError] = err
            return

        # Config file doesn't currently exist
        if ENVIRONMENT.clowder_config_yaml is None or not ENVIRONMENT.clowder_config_yaml.exists():
            self.version: float = CONFIG_VERSION
            current_clowder_config = ClowderConfig(current_clowder_name=current_clowder_name)
            self.clowder_configs: Tuple[ClowderConfig, ...] = (current_clowder_config,)
            self.current_clowder_config: Optional[ClowderConfig] = current_clowder_config
            return

        error_message = f"Clowder config file at {fmt.path(ENVIRONMENT.clowder_config_yaml)} appears to be invalid"
        try:
            # Config file does exist, try to load
            self._load_clowder_config_yaml()
        except Exception as err:
            LOG.error('Failed to load clowder config file')
            if raise_exceptions:
                raise
            self.load_clowder_config_error: Optional[Exception] = err
            LOG.error(error_message)
        finally:
            # If current clowder exists, return
            if self.current_clowder_config is not None:
                return

            # If current clowder config doesn't exist, create empty one
            self.current_clowder_config: Optional[ClowderConfig] = ClowderConfig(
                current_clowder_name=current_clowder_name)
            if not self.clowder_configs:
                self.clowder_configs: Tuple[ClowderConfig, ...] = (self.current_clowder_config,)
            else:
                configs = list(self.clowder_configs)
                configs.append(self.current_clowder_config)
                self.clowder_configs: Tuple[ClowderConfig, ...] = tuple(configs)

    def process_projects_arg(self, projects: List[str]) -> Tuple[str, ...]:
        """Process project args based on parameters and config

        :param List[str] projects: Projects to filter
        :return: Projects in groups matching given names
        """

        if projects != ['default']:
            return tuple(sorted(projects))

        if self.current_clowder_config is None:
            return ('all',)  # noqa

        if self.current_clowder_config.projects is None:
            return ('all',)  # noqa

        return self.current_clowder_config.projects

    def save(self) -> None:
        """Save configuration to file"""

        # If directory doesn't exist, create it
        if not ENVIRONMENT.clowder_config_dir.exists():
            make_dir(ENVIRONMENT.clowder_config_dir)

        # If file doesn't exist, save it
        if not ENVIRONMENT.clowder_config_yaml.is_file():
            save_yaml_file(self._get_yaml(), ENVIRONMENT.clowder_config_yaml)
            return

        # If file does exist, move to .backup
        create_backup_file(ENVIRONMENT.clowder_config_yaml)

        try:
            # Save new file
            remove_file(ENVIRONMENT.clowder_config_yaml)
            save_yaml_file(self._get_yaml(), ENVIRONMENT.clowder_config_yaml)
        except Exception as err:
            LOG.debug('Failed to save configuration file', err)
            # If failed, restore backup
            # TODO: Handle possible exception
            restore_from_backup_file(ENVIRONMENT.clowder_config_yaml)
            raise

    def _get_yaml(self) -> dict:
        """Get yaml representation of config

        :return: YAML python object
        """

        clowder_configs = [c.get_yaml() for c in self.clowder_configs if not c.is_empty()]
        config = {'version': self.version, 'clowder_configs': clowder_configs}
        return config

    def _load_clowder_config_yaml(self) -> None:
        """Load clowder config yaml file"""

        try:
            parsed_yaml = load_yaml_file(ENVIRONMENT.clowder_config_yaml, ENVIRONMENT.clowder_config_dir)
            validate_yaml_file(parsed_yaml, ENVIRONMENT.clowder_config_yaml)

            self.version: float = parsed_yaml['version']

            configs = parsed_yaml['clowder_configs']
            clowder_configs = []
            for config in configs:
                clowder_configs.append(ClowderConfig(clowder_config=config))
            self.clowder_configs: Tuple[ClowderConfig, ...] = tuple(clowder_configs)

            if ENVIRONMENT.clowder_dir is not None:
                for config in self.clowder_configs:
                    if config.clowder_dir.resolve() == ENVIRONMENT.clowder_dir.resolve():
                        self.current_clowder_config: Optional[ClowderConfig] = config
                        self.current_clowder_config.validate_config_projects_defined(self._project_options)
                        break
        except (AttributeError, KeyError, TypeError) as err:
            self.version: float = CONFIG_VERSION
            self.clowder_configs: Tuple[ClowderConfig, ...] = ()
            self.current_clowder_config: Optional[ClowderConfig] = None
            LOG.debug('Failed to load clowder config', err)
            message = f"{fmt.path(ENVIRONMENT.clowder_config_yaml)}\n" \
                      f"Clowder config file appears to be invalid"
            LOG.debug(message)
            raise
