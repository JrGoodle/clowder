# -*- coding: utf-8 -*-
"""Clowder config class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import auto, Enum, unique
from pathlib import Path
from typing import Optional, Tuple

from termcolor import cprint

from clowder import CLOWDER_DIR
from clowder.error import (
    ClowderExit,
    ClowderConfigYAMLError, ClowderConfigYAMLErrorType
)


@unique
class ClowderConfigType(Enum):
    PARALLEL = auto()
    PROJECTS = auto()
    PROTOCOL = auto()
    REBASE = auto()


class ClowderConfig(object):
    """Clowder config class

    :ivar str name: Name of clowder
    :ivar Path clowder_dir: Path to clowder directory
    :ivar Optional[Tuple[str, ...]] projects: Default projects
    :ivar Optional[str] protocol: Default protocol
    :ivar Optional[bool] rebase: Default rebase
    :ivar Optional[bool] parallel: Default parallel
    """

    def __init__(self, clowder_config: Optional[dict] = None,
                 current_clowder_name: Optional[str] = None,
                 project_options: Tuple[str, ...] = ()):
        """Config __init__

        :param Optional[dict] clowder_config: Parsed YAML python object for clowder config
        :param Optional[str] current_clowder_name: Name of current clowder
        :param Tuple[str, ...] project_options: Existing project options from parsed clowder yaml
        Raises:
            ClowderExit
            ClowderConfigYAMLError
        """

        if clowder_config is None:
            self.clowder_dir = CLOWDER_DIR
            self.name = current_clowder_name
            self.parallel = None
            self.projects = None
            self.protocol = None
            self.rebase = None
            return

        self.clowder_dir = Path(clowder_config['clowder_dir'])

        # Validate path is a valid clowder directory
        if not self.clowder_dir.is_dir():
            raise ClowderConfigYAMLError(f"No clowder found at {self.clowder_dir}",
                                         ClowderConfigYAMLErrorType.INVALID_CLOWDER_PATH)

        self.name = clowder_config['name']
        defaults = clowder_config.get('defaults', None)
        if defaults is not None:
            projects = defaults.get('projects', None)
            self.projects: Optional[Tuple[str, ...]] = None if projects is None else tuple(sorted(projects))
            # TODO: Confirm projects exist, otherwise throw error, maybe offer to clean up?
            self.validate_config_projects_defined(self.projects, project_options)
            self.protocol: Optional[str] = defaults.get('protocol', None)
            self.rebase: Optional[bool] = defaults.get('rebase', None)
            self.parallel: Optional[bool] = defaults.get('parallel', None)

    def is_empty(self) -> bool:
        """Determine if any config values are set

        :return: True, if any config values are set
        :rtype: bool
        """

        config_status = [self.is_config_value_set(ClowderConfigType.PARALLEL),
                         self.is_config_value_set(ClowderConfigType.PROJECTS),
                         self.is_config_value_set(ClowderConfigType.PROTOCOL),
                         self.is_config_value_set(ClowderConfigType.REBASE)]
        return not any(config_status)

    def clear(self) -> None:
        """Clear all config settings"""

        self.parallel = None
        self.projects = None
        self.protocol = None
        self.rebase = None

    def get_yaml(self) -> dict:
        """Get yaml representation of config

        :return: YAML python object
        :rtype: dict
        """

        defaults = {}
        if self.projects is not None:
            defaults['projects'] = self.projects
        if self.protocol is not None:
            defaults['protocol'] = self.protocol
        if self.rebase is not None:
            defaults['rebase'] = self.rebase
        if self.parallel is not None:
            defaults['parallel'] = self.parallel
        config = {'clowder_dir': str(self.clowder_dir),
                  'name': self.name,
                  'defaults': defaults}
        return config

    def is_config_value_set(self, value: ClowderConfigType) -> None:
        """Determine if config value is set"""

        if value is ClowderConfigType.PARALLEL:
            return self.parallel is not None
        elif value is ClowderConfigType.PROJECTS:
            return self.projects is not None
        elif value is ClowderConfigType.PROTOCOL:
            return self.protocol is not None
        elif value is ClowderConfigType.REBASE:
            return self.rebase is not None
        else:
            raise ClowderExit(1)

    def print_config_value(self, value: ClowderConfigType) -> None:
        """Print current configuration"""

        if value is ClowderConfigType.PARALLEL:
            if self.parallel is None:
                print(" - parallel not set")
            else:
                print(f" - parallel: {self.parallel}")
        elif value is ClowderConfigType.PROJECTS:
            if self.projects is None:
                print(" - projects not set")
            else:
                print(f" - projects: {', '.join(self.projects)}")
        elif value is ClowderConfigType.PROTOCOL:
            if self.protocol is None:
                print(" - protocol not set")
            else:
                print(f" - protocol: {self.protocol}")
        elif value is ClowderConfigType.REBASE:
            if self.rebase is None:
                print(" - rebase not set")
            else:
                print(f" - rebase: {self.rebase}")
        else:
            raise ClowderExit(1)

    def print_configuration(self) -> None:
        """Print current configuration"""

        cprint('Current config', attrs=['bold'])

        if self.is_empty():
            print(' - No config values set')
            return

        output = ''
        if self.parallel is not None:
            output += f" - parallel: {self.parallel}\n"
        if self.projects is not None:
            output += f" - projects: {', '.join(self.projects)}\n"
        if self.protocol is not None:
            output += f" - protocol: {self.protocol}\n"
        if self.rebase is not None:
            output += f" - rebase: {self.rebase}\n"

        print(output, end='')

    @staticmethod
    def validate_config_projects_defined(project_names: Tuple[str, ...], project_options: Tuple[str, ...]) -> None:
        """Validate all projects were defined in clowder yaml file

        :param Tuple[str, ...] project_names: Project names to validate
        :param Tuple[str, ...] project_options: Projects to validate against
        :raise ClowderConfigYAMLError:
        """

        for project in project_names:
            if project not in project_options:
                raise ClowderConfigYAMLError(f"Unknown project found: {project}",
                                             ClowderConfigYAMLErrorType.MISSING_PROJECT)

        # FIXME: Assemble all undefined projects in message rather than raising on first instance not found
