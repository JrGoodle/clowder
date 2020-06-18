# -*- coding: utf-8 -*-
"""Clowder environment

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.git.util import existing_git_repository


class ClowderEnvironment(object):
    """clowder paths class

    :cvar Path current_dir: Current directory command was run in
    :cvar Path clowder_config_dir: Path to clowder config directory
    :cvar Path clowder_config_yaml: Path to clowder config yaml file
    :cvar Optional[Path] clowder_dir: Path to clowder directory if it exists
    :cvar Optional[Path] clowder_repo_dir: Path to clowder repo directory if it exists
    :cvar Optional[Path] clowder_repo_versaions_dir: Path to clowder repo versions directory
    :cvar Optional[Path] clowder_yaml: Path to clowder yaml file if it exists
    :cvar Optional[ClowderError] clowder_yaml_missing_source_error: Possible error for broken clowder yaml symlink
    :cvar Optional[ClowderError] ambiguous_clowder_yaml_error: Possible error due to ambiguous clowder yaml
    :cvar Optional[ClowderError] clowder_repo_existing_file_error: Possible error due to existing .clowder file
    """

    current_dir = Path.cwd()
    clowder_config_dir = Path.home() / '.config' / 'clowder'
    clowder_config_yaml = clowder_config_dir / 'clowder.config.yml'
    clowder_dir: Optional[Path] = None
    clowder_repo_dir: Optional[Path] = None
    clowder_git_repo_dir: Optional[Path] = None
    clowder_repo_versions_dir: Optional[Path] = None
    clowder_yaml: Optional[Path] = None

    clowder_yaml_missing_source_error: Optional[ClowderError] = None
    ambiguous_clowder_yaml_error: Optional[ClowderError] = None
    clowder_repo_existing_file_error: Optional[ClowderError] = None

    def __init__(self):
        """ClowderEnvironment __init__"""

        self._configure_directories()
        self._configure_clowder_yaml()

    def has_ambiguous_clowder_yaml_files(self) -> bool:
        """Check for ambiguous clowder yaml files

        :return: Whether abmigous clowder yaml files exist
        :rtype: bool
        :raise ClowderError:
        """

        clowder_yml = self._get_possible_yaml_path('clowder.yml')
        clowder_yaml = self._get_possible_yaml_path('clowder.yaml')

        clowder_yml_exists = clowder_yml.is_file() or clowder_yml.is_symlink()
        clowder_yaml_exists = clowder_yaml.is_file() or clowder_yaml.is_symlink()
        has_ambiguous_clowder_yaml_files = clowder_yml_exists and clowder_yaml_exists

        if has_ambiguous_clowder_yaml_files:
            self.ambiguous_clowder_yaml_error = ClowderError(ClowderErrorType.AMBIGUOUS_CLOWDER_YAML,
                                                             fmt.error_ambiguous_clowder_yaml())
        else:
            self.ambiguous_clowder_yaml_error = None

        return has_ambiguous_clowder_yaml_files

    def _configure_clowder_yaml(self) -> None:
        """Configure clowder yaml file environment variables"""

        if self.has_ambiguous_clowder_yaml_files():
            return

        clowder_yml = self._get_possible_yaml_path('clowder.yml')
        clowder_yaml = self._get_possible_yaml_path('clowder.yaml')

        self._set_clowder_yaml(clowder_yml)
        self._set_clowder_yaml(clowder_yaml)

    def _configure_directories(self) -> None:
        """Configure clowder directories environment variables"""

        # Walk up directory tree to find possible .clowder directory,
        # clowder.yml file, or clowder.yaml and set environment variables

        path = Path.cwd()
        while str(path) != path.root:
            clowder_repo_dir = path / '.clowder'
            clowder_yml = path / 'clowder.yml'
            clowder_yaml = path / 'clowder.yaml'
            clowder_yml_exists = clowder_yml.is_file() or clowder_yml.is_symlink()
            clowder_yaml_exists = clowder_yaml.is_file() or clowder_yaml.is_symlink()
            clowder_repo_file_exists = clowder_repo_dir.is_symlink() or clowder_repo_dir.is_file()
            if clowder_repo_dir.is_dir() and existing_git_repository(clowder_repo_dir):
                self.clowder_dir = path
                self.clowder_repo_dir = clowder_repo_dir.resolve()
                self.clowder_git_repo_dir = clowder_repo_dir
                break
            elif clowder_repo_dir.is_dir():
                self.clowder_dir = path
                self.clowder_repo_dir = clowder_repo_dir.resolve()
                break
            elif clowder_yml_exists or clowder_yaml_exists or clowder_repo_file_exists:
                if clowder_repo_file_exists:
                    self.clowder_repo_existing_file_error = ClowderError(ClowderErrorType.CLOWDER_REPO_EXISTING_FILE,
                                                                         fmt.error_existing_file_at_clowder_repo_path(
                                                                             clowder_repo_dir))
                self.clowder_dir = path
                break
            path = path.parent

        if self.clowder_repo_dir is not None:
            clowder_versions = self.clowder_repo_dir / 'versions'
            if clowder_versions.is_dir():
                self.clowder_repo_versions_dir = clowder_versions

    def _get_possible_yaml_path(self, name: str) -> Path:
        """Get possible yaml path based on other environment variables

        :param Path name: Name of file to return
        :return: Path to possible exsting yaml file
        :rtype: Path
        """

        if self.clowder_dir is not None:
            return self.clowder_dir / name

        return self.current_dir / name

    def _set_clowder_yaml(self, yaml_file: Path) -> None:
        """Set clowder yaml variable if file exists

        :param Path yaml_file: Path to clowder yaml file
        """

        # Symlink pointing to existing source
        if yaml_file.is_symlink() and yaml_file.exists():
            self.clowder_yaml = yaml_file
            return

        # Broken symlink pointing to missing source
        if yaml_file.is_symlink() and not yaml_file.exists():
            message = fmt.error_clowder_symlink_source_missing(yaml_file)
            self.clowder_yaml_missing_source_error = ClowderError(ClowderErrorType.CLOWDER_SYMLINK_SOURCE_MISSING,
                                                                  message)
            return

        # Existing non-symlink file
        if not yaml_file.is_symlink() and yaml_file.is_file():
            self.clowder_yaml = yaml_file
            return


ENVIRONMENT = ClowderEnvironment()
