"""Representation of clowder yaml project

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Optional, Set

import pygoodle.command as cmd
from pygoodle.format import Format
from pygoodle.git import Branch, Protocol, Ref

from clowder.log import LOG
from clowder.environment import ENVIRONMENT
from clowder.util.error import DuplicateRemoteError

from .resolved_git_settings import ResolvedGitSettings
from .resolved_upstream import ResolvedUpstream
from .source_controller import SOURCE_CONTROLLER, GITHUB
from .model import Defaults, Project, Source, Section


class ResolvedProject:
    """clowder yaml Project model class

    :ivar str name: Project name
    :ivar Path path: Project relative path
    :ivar Set[str] groups: Groups project belongs to
    :ivar str remote: Project remote name
    :ivar Source source: Project source
    :ivar ResolvedGitSettings git_settings: Custom git settings
    :ivar Optional[ResolvedUpstream] upstream: Project's associated upstream
    :ivar Optional[str] ref: Project git ref
    :ivar Optional[GitProtocol] default_protocol: Default git protocol to use
    """

    def __init__(self, project: Project, defaults: Optional[Defaults] = None,
                 section: Optional[Section] = None, protocol: Optional[Protocol] = None):
        """Project __init__

        :param Project project: Project model instance
        :param Optional[Defaults] defaults: Defaults instance
        :param Optional[Section] section: Section instance
        :raise DuplicateRemoteError:
        """

        project.resolved_project_id = id(self)
        self.name: str = project.name

        has_path = project.path is not None
        has_section = section is not None
        has_group_path = has_section and section.path is not None
        self.path: Path = section.path if has_group_path else Path()
        if has_path:
            self.path: Path = self.path / project.path
        else:
            self.path: Path = self.path / Path(self.name).name

        self.remote: str = self._get_property('remote', project, defaults, section, default='origin')
        self.ref: Optional[Ref] = self._get_property('git_ref', project, defaults, section)
        self.git_settings: ResolvedGitSettings = ResolvedGitSettings.combine_settings(project, section, defaults)

        source = self._get_property('source', project, defaults, section, default=GITHUB)
        self.source: Source = SOURCE_CONTROLLER.get_source(source)

        self.default_protocol: Optional[Protocol] = None
        if self.source.protocol is not None:
            self.default_protocol: Optional[Protocol] = self.source.protocol
        elif protocol is not None:
            self.default_protocol: Optional[Protocol] = protocol

        self.upstream: Optional[ResolvedUpstream] = None
        if project.upstream is not None:
            self.upstream: Optional[ResolvedUpstream] = ResolvedUpstream(self.path, project.upstream,
                                                                         defaults, section, protocol)
            if self.remote == self.upstream.remote:
                message = f"{Format.path(ENVIRONMENT.clowder_yaml.name)} appears to be invalid\n" \
                          f"{Format.path(ENVIRONMENT.clowder_yaml)}\n" \
                          f"upstream '{self.upstream.name}' and project '{self.name}' " \
                          f"have same remote name '{self.remote}'"
                raise DuplicateRemoteError(message)

        self.groups: Set[str] = {'all', self.name, str(self.path)}
        if has_section:
            self.groups.add(section.name)
            if section.groups is not None:
                self.groups.update({g for g in section.groups})
        if project.groups is not None:
            self.groups.update(set(project.groups))
        if 'notdefault' in self.groups:
            self.groups.remove('all')

    @property
    def full_path(self) -> Path:
        """Full path to project"""

        return ENVIRONMENT.clowder_dir / self.path

    # def formatted_project_output(self) -> str:
    #     """Return formatted project path/name
    #
    #     :return: Formatted string of full file path if cloned, otherwise project name
    #     """
    #
    #     if existing_git_repo(self.full_path):
    #         return str(self.path)
    #
    #     return self.name

    # def print_existence_message(self) -> None:
    #     """Print existence validation message for project"""
    #
    #     if not existing_git_repo(self.full_path):
    #         CONSOLE.stdout(self.status())

    def update_default_branch(self, branch: str) -> None:
        """Update ref with default branch if none set"""

        if self.ref is None:
            self.ref = Branch(self.full_path, branch)

    @property
    def url(self) -> str:
        """Project url"""

        if self.source.protocol is not None:
            protocol = self.source.protocol
        elif SOURCE_CONTROLLER.protocol_override is not None:
            protocol = SOURCE_CONTROLLER.protocol_override
        elif self.default_protocol is not None:
            protocol = self.default_protocol
        else:
            protocol = SOURCE_CONTROLLER.get_default_protocol()

        return protocol.format_url(self.source.url, self.name)

    def _run_forall_command(self, command: str, env: dict, check: bool) -> None:
        """Run command or script in project directory

        :param str command: Command to run
        :param dict env: Environment variables
        :param bool check: Whether to exit if command returns a non-zero exit code
        """

        try:
            cmd.run(command, self.full_path, env=env, print_command=True)
        except CalledProcessError as err:
            if check:
                LOG.error(f'Command failed: {command}')
                raise
            LOG.debug(f'Command failed: {command}', err)

    @staticmethod
    def _get_property(name: str, project: Project, defaults: Optional[Defaults], section: Optional[Section],
                      default: Optional[Any] = None) -> Optional[Any]:
        project_value = getattr(project, name)
        has_defaults = defaults is not None
        defaults_value = getattr(defaults, name) if has_defaults else None
        has_section = section is not None
        has_section_defaults = has_section and section.defaults is not None
        section_defaults_value = getattr(section.defaults, name) if has_section_defaults else None
        if project_value is not None:
            return project_value
        elif section_defaults_value is not None:
            return section_defaults_value
        elif defaults_value is not None:
            return defaults_value
        elif default is not None:
            return default
        else:
            return None
