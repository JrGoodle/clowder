"""Clowder config class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, Enum, unique
from pathlib import Path
from typing import Optional, Tuple

import clowder.util.formatting as fmt
from clowder.console import CONSOLE
from clowder.environment import ENVIRONMENT
from clowder.error import *
from clowder.git_project import GitProtocol


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
    :ivar Optional[GitProtocol] protocol: Default protocol
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
            self.clowder_dir: Path = ENVIRONMENT.clowder_dir
            self.name: str = current_clowder_name
            self.jobs: Optional[int] = None
            self.projects: Optional[Tuple[str, ...]] = None
            self.protocol: Optional[GitProtocol] = None
            self.rebase: Optional[bool] = None
            return

        self.clowder_dir: Path = Path(clowder_config['clowder_dir'])

        # Validate path is a valid clowder directory
        if not self.clowder_dir.is_dir():
            raise ClowderError(f"No clowder found at {self.clowder_dir}")

        self.name: str = clowder_config['name']
        defaults = clowder_config.get('defaults', None)
        if defaults is not None:
            projects = defaults.get('projects', None)
            self.projects: Optional[Tuple[str, ...]] = None if projects is None else tuple(sorted(projects))
            protocol = defaults.get('protocol', None)
            self.protocol: Optional[GitProtocol] = None if protocol is None else GitProtocol(protocol)
            self.rebase: Optional[bool] = defaults.get('rebase', None)
            self.jobs: Optional[int] = defaults.get('jobs', None)

    def is_empty(self) -> bool:
        """Determine if any config values are set

        :return: True, if any config values are set
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
        """

        defaults = {}
        if self.projects is not None:
            defaults['projects'] = self.projects
        if self.protocol is not None:
            defaults['protocol'] = self.protocol.value
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
        :raise UnknownTypeError:
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
            raise UnknownTypeError("Unknown config type")

    def print_config_value(self, value: ClowderConfigType) -> None:
        """Print current configuration

        :param ClowderConfigType value: Clowder config value
        :raise UnknownTypeError:
        """

        if value is ClowderConfigType.JOBS:
            if self.jobs is None:
                CONSOLE.stdout(" - jobs not set")
            else:
                CONSOLE.stdout(f" - jobs: {self.jobs}")
        elif value is ClowderConfigType.PROJECTS:
            if self.projects is None:
                CONSOLE.stdout(" - projects not set")
            else:
                CONSOLE.stdout(f" - projects: {', '.join(self.projects)}")
        elif value is ClowderConfigType.PROTOCOL:
            if self.protocol is None:
                CONSOLE.stdout(" - protocol not set")
            else:
                CONSOLE.stdout(f" - protocol: {self.protocol.value}")
        elif value is ClowderConfigType.REBASE:
            if self.rebase is None:
                CONSOLE.stdout(" - rebase not set")
            else:
                CONSOLE.stdout(f" - rebase: {self.rebase}")
        else:
            raise UnknownTypeError("Unknown config type")

    def print_configuration(self) -> None:
        """Print current configuration"""

        CONSOLE.stdout(fmt.bold('Current config\n'))
        if self.is_empty():
            CONSOLE.stdout(' - No config values set')
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

        CONSOLE.stdout(output)

    def validate_config_projects_defined(self, project_options: Tuple[str, ...]) -> None:
        """Validate all projects were defined in clowder yaml file

        :param Tuple[str, ...] project_options: Projects to validate against
        :raise UnknownProjectError:
        """

        if self.projects is None:
            return

        for project in self.projects:
            if project not in project_options:
                message = f"{fmt.path(ENVIRONMENT.clowder_config_yaml)}\n" \
                          f"Clowder config file appears to be invalid" \
                          f"Unknown project {fmt.project_name(project)}"
                raise UnknownProjectError(message)

        # FIXME: Assemble all undefined projects in message rather than raising on first instance not found
