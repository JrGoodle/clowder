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
    :cvar Optional[ClowderError] CLOWDER_YAML_ERROR: Possible error loading clowder yaml file
    """

    current_dir = Path.cwd()
    clowder_config_dir = Path.home() / '.config' / 'clowder'
    clowder_config_yaml = clowder_config_dir / 'clowder.config.yml'
    clowder_dir: Optional[Path] = None
    clowder_repo_dir: Optional[Path] = None
    clowder_git_repo_dir: Optional[Path] = None
    clowder_repo_versions_dir: Optional[Path] = None
    clowder_yaml: Optional[Path] = None

    clowder_yaml_error: Optional[ClowderError] = None

    def __init__(self):
        """ClowderEnvironment __init__"""

        self.configure_directories()
        self.configure_clowder_yaml()

    def configure_directories(self) -> None:
        """Configure clowder directories"""

        # Walk up directory tree to find possible .clowder directory,
        # clowder.yml file, or clowder.yaml and set environment variables

        path = Path.cwd()
        while str(path) != path.root:
            clowder_repo_dir = path / '.clowder'
            clowder_yml = path / 'clowder.yml'
            clowder_yaml = path / 'clowder.yaml'
            if clowder_repo_dir.is_dir() and existing_git_repository(clowder_repo_dir):
                self.clowder_dir = path
                self.clowder_repo_dir = clowder_repo_dir
                self.clowder_git_repo_dir = clowder_repo_dir
                break
            elif clowder_repo_dir.is_dir():
                self.clowder_dir = path
                self.clowder_repo_dir = clowder_repo_dir
                break
            elif clowder_yml.is_file() or clowder_yaml.is_file():
                self.clowder_dir = path
                break
            path = path.parent

        if self.clowder_repo_dir is not None:
            clowder_versions = self.clowder_repo_dir / 'versions'
            if clowder_versions.is_dir():
                self.clowder_repo_versions_dir = clowder_versions

    def configure_clowder_yaml(self) -> None:
        """Configure clowder directories"""

        # If clowder directory exists, try to set other environment path variables
        if self.clowder_dir is not None:
            clowder_yml = self.clowder_dir / 'clowder.yml'
            clowder_yaml = self.clowder_dir / 'clowder.yaml'
        else:
            clowder_yml = self.current_dir / 'clowder.yml'
            clowder_yaml = self.current_dir / 'clowder.yaml'

        if clowder_yml.is_file() and clowder_yaml.is_file():
            self.clowder_yaml_error = ClowderError(ClowderErrorType.AMBIGUOUS_CLOWDER_YAML,
                                                   fmt.error_ambiguous_clowder_yaml())
            return

        self._configure_clowder_yaml(clowder_yml)
        self._configure_clowder_yaml(clowder_yaml)

    def _configure_clowder_yaml(self, yaml_file: Path) -> None:
        """Configure clowder directories

        :param Path yaml_file: Path to clowder yaml file
        """

        if not yaml_file.is_file():
            return

        if not yaml_file.is_symlink():
            self.clowder_yaml = yaml_file
            return

        if yaml_file.exists():
            self.clowder_yaml = yaml_file
            return

        message = fmt.error_clowder_symlink_source_missing(yaml_file, self.clowder_dir)
        self.clowder_yaml_error = ClowderError(ClowderErrorType.CLOWDER_SYMLINK_SOURCE_MISSING, message)


ENVIRONMENT = ClowderEnvironment()
