"""Clowder environment

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import pkg_resources
from functools import wraps
from pathlib import Path
from typing import Optional

from pygoodle.format import Format
from pygoodle.git.offline import GitOffline

from clowder.util.error import (
    AmbiguousYamlError,
    ExistingFileError,
    MissingSourceError,
    MissingClowderRepoError,
    MissingClowderGitRepoError
)


def clowder_repo_required(func):
    """If no clowder repo exists, print clowder repo not found message and exit

    :raise ExistingFileError:
    :raise MissingClowderGitRepo:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.existing_clowder_repo_file_error is not None:
            raise ENVIRONMENT.existing_clowder_repo_file_error
        if ENVIRONMENT.clowder_repo_dir is None:
            raise MissingClowderRepoError(f"No {Format.path(Path('.clowder'))} directory found")

        return func(*args, **kwargs)

    return wrapper


def clowder_git_repo_required(func):
    """If no clowder git repo exists, print clowder git repo not found message and exit

    :raise MissingClowderGitRepo:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir is None:
            raise MissingClowderGitRepoError(f"No {Format.path(Path('.clowder'))} git repository found")
        return func(*args, **kwargs)

    return wrapper


class ClowderEnvironment:
    """clowder paths class

    :cvar Path current_dir: Current directory command was run in
    :cvar Path clowder_config_dir: Path to clowder config directory
    :cvar Path clowder_config: Path to clowder config yaml file
    :cvar Optional[Path] clowder_dir: Path to clowder directory if it exists
    :cvar Optional[Path] clowder_repo_dir: Path to clowder repo directory if it exists
    :cvar Optional[Path] clowder_repo_versaions_dir: Path to clowder repo versions directory
    :cvar Optional[Path] clowder_repo_plugins_dir: Path to clowder repo plugins directory
    :cvar Optional[Path] clowder_yaml: Path to clowder yaml file if it exists

    :cvar Optional[MissingSourceError] missing_source_error: Possible error for broken clowder yaml symlink
    :cvar Optional[AmbiguousYamlError] ambiguous_yaml_error: Possible error due to ambiguous clowder yaml
    :cvar Optional[ExistingFileError] existing_clowder_repo_file_error: Possible error due to existing .clowder file
    """

    current_dir: Path = Path.cwd()
    clowder_config_dir: Optional[Path] = None
    clowder_config: Optional[Path] = None
    clowder_dir: Optional[Path] = None
    clowder_repo_dir: Optional[Path] = None
    clowder_git_repo_dir: Optional[Path] = None
    clowder_repo_versions_dir: Optional[Path] = None
    clowder_repo_plugins_dir: Optional[Path] = None
    clowder_yaml: Optional[Path] = None

    missing_source_error: Optional[MissingSourceError] = None
    ambiguous_yaml_error: Optional[AmbiguousYamlError] = None
    existing_clowder_repo_file_error: Optional[ExistingFileError] = None

    def __init__(self):
        """ClowderEnvironment __init__"""

        self.clowder_schema: str = pkg_resources.resource_string(__name__, 'clowder.schema.json')
        self._configure_directories()
        self._configure_clowder_yaml()

    def has_ambiguous_clowder_yaml_files(self) -> bool:
        """Check for ambiguous clowder yaml files

        :return: Whether abmigous clowder yaml files exist
        """

        clowder_yml = self._get_possible_yaml_path('clowder.yml')
        clowder_yaml = self._get_possible_yaml_path('clowder.yaml')

        clowder_yml_exists = clowder_yml.is_file() or clowder_yml.is_symlink()
        clowder_yaml_exists = clowder_yaml.is_file() or clowder_yaml.is_symlink()
        has_ambiguous_clowder_yaml_files = clowder_yml_exists and clowder_yaml_exists

        if has_ambiguous_clowder_yaml_files:
            yml_file = Format.path(Path('clowder.yml'))
            yaml_file = Format.path(Path('clowder.yaml'))
            message = f"Found {yml_file} and {yaml_file} files in same directory"
            self.ambiguous_yaml_error = AmbiguousYamlError(message)
        else:
            self.ambiguous_yaml_error = None

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
            if GitOffline.is_repo_cloned(clowder_repo_dir):
                self.clowder_dir: Optional[Path] = path
                self.clowder_repo_dir: Optional[Path] = clowder_repo_dir.resolve()
                self.clowder_git_repo_dir: Optional[Path] = clowder_repo_dir
                break
            elif clowder_repo_dir.is_dir():
                self.clowder_dir: Optional[Path] = path
                self.clowder_repo_dir: Optional[Path] = clowder_repo_dir.resolve()
                break
            elif clowder_yml_exists or clowder_yaml_exists or clowder_repo_file_exists:
                # FIXME: Is this right?
                if clowder_repo_file_exists:
                    message = f"Found non-directory file {Format.path(clowder_repo_dir)} " \
                              f"where clowder repo directory should be"
                    self.existing_clowder_repo_file_error: Optional[ExistingFileError] = ExistingFileError(message)
                self.clowder_dir: Optional[Path] = path
                break
            path = path.parent

        if self.clowder_dir is not None:
            self.clowder_config: Optional[Path] = self.clowder_dir / 'clowder.config'

        if self.clowder_repo_dir is not None:
            self.clowder_repo_versions_dir: Optional[Path] = self.clowder_repo_dir / 'versions'
            self.clowder_config_dir: Optional[Path] = self.clowder_repo_dir / "config"
            self.clowder_repo_plugins_dir: Optional[Path] = self.clowder_repo_dir / "plugins"

    def _get_possible_yaml_path(self, name: str) -> Path:
        """Get possible yaml path based on other environment variables

        :param Path name: Name of file to return
        :return: Path to possible exsting yaml file
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
            self.clowder_yaml: Optional[Path] = yaml_file
            return

        # Broken symlink pointing to missing source
        if yaml_file.is_symlink() and not yaml_file.exists():
            message = f"Found symlink {Format.path(yaml_file)} but " \
                      f"source {Format.path((yaml_file.resolve()))} appears to be missing"
            self.missing_source_error: Optional[MissingSourceError] = MissingSourceError(message)
            return

        # Existing non-symlink file
        if not yaml_file.is_symlink() and yaml_file.is_file():
            self.clowder_yaml: Optional[Path] = yaml_file
            return


ENVIRONMENT = ClowderEnvironment()
