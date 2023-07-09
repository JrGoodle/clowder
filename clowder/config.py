"""Clowder config class

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from configparser import ConfigParser
from enum import auto, unique
from functools import wraps
from typing import Any, List, Optional, Tuple

import clowder.util.filesystem as fs
from clowder.util.console import CONSOLE
from clowder.util.enum import AutoLowerName
from clowder.util.format import Format
from clowder.util.git import Protocol

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.util.error import MissingFileError, UnknownProjectError


def print_config(func):
    """Print config after wrapped function returrns"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""
        retval = func(*args, **kwargs)
        Config().print_config()
        return retval

    return wrapper


@unique
class CommandConfigType(AutoLowerName):
    JOBS = auto()
    PROJECTS = auto()

    @staticmethod
    def section_name() -> str:
        return 'command'


@unique
class GitConfigType(AutoLowerName):
    FETCH = auto()
    PROTOCOL = auto()
    REBASE = auto()

    @classmethod
    def section_name(cls) -> str:
        return 'git'


class Config:
    """Config class

    :ivar str name: Name of clowder
    :ivar Optional[Tuple[str, ...]] projects: Default projects
    :ivar Optional[GitProtocol] protocol: Default protocol
    :ivar Optional[bool] rebase: Default rebase
    :ivar Optional[int] jobs: Default number of jobs
    """

    def __init__(self):
        """Config __init__"""

        self._config: ConfigParser = ConfigParser()

        if ENVIRONMENT.clowder_config is not None and ENVIRONMENT.clowder_config.exists():
            self._config.read(ENVIRONMENT.clowder_config)

        git_section = GitConfigType.section_name()
        if git_section not in self._config:
            self._config[git_section] = {}
        self._git_config = self._config[git_section]

        command_section = CommandConfigType.section_name()
        if command_section not in self._config:
            self._config[command_section] = {}
        self._command_config = self._config[command_section]

        self._validate_config_projects_defined(self.projects)

        # if defaults is not None:
        #     projects = defaults.get('projects', None)
        #     self.projects: Optional[Tuple[str, ...]] = None if projects is None else tuple(sorted(projects))
        #     protocol = defaults.get('protocol', None)
        #     self.protocol: Optional[GitProtocol] = None if protocol is None else GitProtocol(protocol)
        #     self.rebase: Optional[bool] = defaults.get('rebase', None)
        #     self.jobs: Optional[int] = defaults.get('jobs', None)

    @property
    def jobs(self) -> Optional[int]:
        jobs = str(CommandConfigType.JOBS.value)
        return self._command_config.getint(jobs)

    @jobs.setter
    def jobs(self, jobs: Optional[int]):
        self._set_command_option(CommandConfigType.JOBS, jobs)

    @property
    def projects(self) -> Optional[Tuple[str, ...]]:
        projects = self._command_config.get(str(CommandConfigType.PROJECTS.value))
        if projects is None:
            return None
        projects = [p for p in projects.strip().split(", ")]
        return tuple(sorted(projects))

    @projects.setter
    def projects(self, projects: Optional[List[str]]):
        if not projects:
            self._set_command_option(CommandConfigType.PROJECTS, None)
            return
        self._set_command_option(CommandConfigType.PROJECTS, ", ".join(projects))

    @property
    def protocol(self) -> Optional[Protocol]:
        protocol = str(GitConfigType.PROTOCOL.value)
        protocol = self._git_config.get(protocol)
        if protocol is None:
            return None
        return Protocol(protocol)

    @protocol.setter
    def protocol(self, protocol: Optional[Protocol]):
        self._set_git_option(GitConfigType.PROTOCOL, protocol.value)

    @property
    def rebase(self) -> Optional[bool]:
        rebase = str(GitConfigType.REBASE.value)
        return self._git_config.getboolean(rebase)

    @rebase.setter
    def rebase(self, rebase: Optional[bool]):
        self._set_git_option(GitConfigType.REBASE, rebase)

    @staticmethod
    def clear() -> None:
        """Clear all config settings"""

        if ENVIRONMENT.clowder_config is not None and ENVIRONMENT.clowder_config.exists():
            fs.remove_file(ENVIRONMENT.clowder_config)

    @staticmethod
    def print_config() -> None:
        """Print current config file contents"""

        if ENVIRONMENT.clowder_config is None or not ENVIRONMENT.clowder_config.exists():
            CONSOLE.stdout(' - No config file found')
            return

        CONSOLE.stdout(Format.bold('Current config\n'))
        text = ENVIRONMENT.clowder_config.read_text()
        CONSOLE.stdout(Format.escape(f"{text.strip()}\n"))

    def process_projects_arg(self, projects: List[str]) -> Tuple[str, ...]:
        """Process project args based on parameters and config

        :param List[str] projects: Projects to filter
        :return: Projects in groups matching given names
        """

        if projects != ['default']:
            return tuple(sorted(projects))

        if not self.projects:
            return ('all',)  # noqa

        return self.projects

    def save(self) -> None:
        """Save configuration to file"""

        # if not ENVIRONMENT.clowder_config_dir.exists():
        #     make_dir(ENVIRONMENT.clowder_config_dir)

        if ENVIRONMENT.clowder_config is None:
            raise MissingFileError('No clowder config file path found')

        with open(ENVIRONMENT.clowder_config, 'w') as configfile:
            self._config.write(configfile)

    def _set_command_option(self, option: CommandConfigType, value: Optional[Any]) -> None:
        if value is None:
            self._config.remove_option(CommandConfigType.section_name(), option.value)
        else:
            self._command_config[option.value] = str(value)

    def _set_git_option(self, option: GitConfigType, value: Optional[Any]) -> None:
        if value is None:
            self._config.remove_option(GitConfigType.section_name(), option.value)
        else:
            self._git_config[option.value] = str(value)

    def _validate_config_projects_defined(self, project_options: Tuple[str, ...]) -> None:
        """Validate all projects were defined in clowder yaml file

        :param Tuple[str, ...] project_options: Projects to validate against
        :raise UnknownProjectError:
        """

        if self.projects is None:
            return

        for project in self.projects:
            if project not in project_options:
                message = f"{Format.path(ENVIRONMENT.clowder_config)}\n" \
                          f"Clowder config file appears to be invalid" \
                          f"Unknown project {fmt.project_name(project)}"
                raise UnknownProjectError(message)

        # FIXME: Assemble all undefined projects in message rather than raising on first instance not found
