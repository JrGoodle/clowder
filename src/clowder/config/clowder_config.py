# -*- coding: utf-8 -*-
"""Clowder config class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import auto, Enum, unique
from pathlib import Path
from typing import Optional, Tuple

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType


@unique
class ClowderConfigType(Enum):
    JOBS = auto()
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
    :ivar Optional[int] jobs: Default number of jobs
    """

    def __init__(self, clowder_config: Optional[dict] = None,
                 current_clowder_name: Optional[str] = None):
        """Config __init__

        :param Optional[dict] clowder_config: Parsed YAML python object for clowder config
        :param Optional[str] current_clowder_name: Name of current clowder
        :raise ClowderError:
        """

        if clowder_config is None:
            self.clowder_dir = ENVIRONMENT.clowder_dir
            self.name = current_clowder_name
            self.jobs = None
            self.projects = None
            self.protocol = None
            self.rebase = None
            return

        self.clowder_dir = Path(clowder_config['clowder_dir'])

        # Validate path is a valid clowder directory
        if not self.clowder_dir.is_dir():
            raise ClowderError(ClowderErrorType.CONFIG_YAML_INVALID_CLOWDER_PATH,
                               fmt.error_no_clowder_found(self.clowder_dir))

        self.name: str = clowder_config['name']
        defaults = clowder_config.get('defaults', None)
        if defaults is not None:
            projects = defaults.get('projects', None)
            self.projects: Optional[Tuple[str, ...]] = None if projects is None else tuple(sorted(projects))
            self.protocol: Optional[str] = defaults.get('protocol', None)
            self.rebase: Optional[bool] = defaults.get('rebase', None)
            self.jobs: Optional[int] = defaults.get('jobs', None)

    def is_empty(self) -> bool:
        """Determine if any config values are set

        :return: True, if any config values are set
        :rtype: bool
        """

        config_status = [self.is_config_value_set(ClowderConfigType.JOBS),
                         self.is_config_value_set(ClowderConfigType.PROJECTS),
                         self.is_config_value_set(ClowderConfigType.PROTOCOL),
                         self.is_config_value_set(ClowderConfigType.REBASE)]
        return not any(config_status)

    def clear(self) -> None:
        """Clear all config settings"""

        self.jobs = None
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
        if self.jobs is not None:
            defaults['jobs'] = self.jobs
        config = {'clowder_dir': str(self.clowder_dir),
                  'name': self.name,
                  'defaults': defaults}
        return config

    def is_config_value_set(self, value: ClowderConfigType) -> None:
        """Determine if config value is set

        :param ClowderConfigType value: Clowder config value
        :raise ClowderError:
        """

        if value is ClowderConfigType.JOBS:
            return self.jobs is not None
        elif value is ClowderConfigType.PROJECTS:
            return self.projects is not None
        elif value is ClowderConfigType.PROTOCOL:
            return self.protocol is not None
        elif value is ClowderConfigType.REBASE:
            return self.rebase is not None
        else:
            raise ClowderError(ClowderErrorType.UNKNOWN_CONFIG_TYPE, fmt.error_unknown_config_type())

    def print_config_value(self, value: ClowderConfigType) -> None:
        """Print current configuration

        :param ClowderConfigType value: Clowder config value
        :raise ClowderError:
        """

        if value is ClowderConfigType.JOBS:
            if self.jobs is None:
                print(" - jobs not set")
            else:
                print(f" - jobs: {self.jobs}")
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
            raise ClowderError(ClowderErrorType.UNKNOWN_CONFIG_TYPE, fmt.error_unknown_config_type())

    def print_configuration(self) -> None:
        """Print current configuration"""

        cprint('Current config', attrs=['bold'])
        print()
        if self.is_empty():
            print(' - No config values set')
            return

        output = ''
        if self.jobs is not None:
            output += f" - jobs: {self.jobs}\n"
        if self.projects is not None:
            output += f" - projects: {', '.join(self.projects)}\n"
        if self.protocol is not None:
            output += f" - protocol: {self.protocol}\n"
        if self.rebase is not None:
            output += f" - rebase: {self.rebase}\n"

        print(output, end='')

    def validate_config_projects_defined(self, project_options: Tuple[str, ...]) -> None:
        """Validate all projects were defined in clowder yaml file

        :param Tuple[str, ...] project_options: Projects to validate against
        :raise ClowderError:
        """

        if self.projects is None:
            return

        for project in self.projects:
            if project not in project_options:
                messages = [f"{fmt.error_invalid_config_file(ENVIRONMENT.clowder_config_yaml)}",
                            f"{fmt.error_unknown_project(project)}"]
                raise ClowderError(ClowderErrorType.CONFIG_YAML_UNKNOWN_PROJECT, messages)

        # FIXME: Assemble all undefined projects in message rather than raising on first instance not found
