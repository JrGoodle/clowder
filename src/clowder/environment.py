# -*- coding: utf-8 -*-
"""Clowder environment

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

import clowder.util.formatting as fmt
from clowder.error import ClowderError, ClowderErrorType
from clowder.git.util import existing_clowder_repo


class ClowderEnvironment(object):
    """clowder paths class

    :cvar Path CURRENT_DIR: Current directory command was run in
    :cvar Path CLOWDER_CONFIG_DIR: Path to clowder config directory
    :cvar Path CLOWDER_CONFIG_YAML: Path to clowder config yaml file
    :cvar Optional[Path] CLOWDER_DIR: Path to clowder directory if it exists
    :cvar Optional[Path] CLOWDER_REPO_DIR: Path to clowder repo directory if it exists
    :cvar Optional[Path] CLOWDER_REPO_VERSIONS_DIR: Path to clowder repo versions directory
    :cvar Optional[Path] CLOWDER_YAML:
    :cvar Optional[ClowderError] CLOWDER_YAML_ERROR:
    """

    CURRENT_DIR = Path.cwd()
    CLOWDER_CONFIG_DIR = Path.home() / '.config' / 'clowder'
    CLOWDER_CONFIG_YAML = CLOWDER_CONFIG_DIR / 'clowder.config.yml'
    CLOWDER_DIR: Optional[Path] = None
    CLOWDER_REPO_DIR: Optional[Path] = None
    CLOWDER_REPO_VERSIONS_DIR: Optional[Path] = None
    CLOWDER_YAML: Optional[Path] = None

    CLOWDER_YAML_ERROR: Optional[ClowderError] = None

    def __init__(self):
        """ClowderEnvironment __init__"""

        self.configure_directories()
        self.configure_clowder_yaml()

        if self.CLOWDER_REPO_DIR is not None and self.CLOWDER_YAML is not None and not self.CLOWDER_YAML.is_symlink():
            print(fmt.warning_clowder_yaml_not_symlink_with_clowder_repo(self.CLOWDER_YAML.name))

    def configure_directories(self) -> None:
        """Configure clowder directories"""

        # Walk up directory tree to find possible clowder repo (.clowder directory) and set global variable
        path = Path.cwd()
        while str(path) != path.root:
            clowder_repo_dir = path / '.clowder'
            if existing_clowder_repo(clowder_repo_dir):
                self.CLOWDER_DIR = path
                self.CLOWDER_REPO_DIR = clowder_repo_dir
                break
            path = path.parent

        clowder_versions = self.CLOWDER_REPO_DIR / 'versions'
        if clowder_versions.is_dir():
            self.CLOWDER_REPO_VERSIONS_DIR = clowder_versions

    def configure_clowder_yaml(self) -> None:
        """Configure clowder directories"""

        # If clowder repo exists, try to set other global path variables
        if self.CLOWDER_REPO_DIR is not None:
            clowder_yml = self.CLOWDER_DIR / 'clowder.yml'
            clowder_yaml = self.CLOWDER_DIR / 'clowder.yaml'
        else:
            clowder_yml = self.CURRENT_DIR / 'clowder.yml'
            clowder_yaml = self.CURRENT_DIR / 'clowder.yaml'

        if clowder_yml.is_file() and clowder_yaml.is_file():
            self.CLOWDER_YAML_ERROR = ClowderError(ClowderErrorType.AMBIGUOUS_CLOWDER_YAML,
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
            self.CLOWDER_YAML = yaml_file
            return

        if yaml_file.exists():
            self.CLOWDER_YAML = yaml_file
            return

        message = fmt.error_clowder_symlink_source_missing(yaml_file, self.CLOWDER_DIR)
        self.CLOWDER_YAML_ERROR = ClowderError(ClowderErrorType.CLOWDER_SYMLINK_SOURCE_MISSING, message)


ENVIRONMENT = ClowderEnvironment()
