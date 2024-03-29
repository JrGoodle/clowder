"""Representation of clowder yaml git settings

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import copy
from typing import Dict, Optional

from clowder.util.git import GitConfig

from clowder.model import Defaults, Section, Project, GitSettings
from clowder.util.error import UnknownArgumentError, UnknownTypeError


class ResolvedGitSettings:
    """clowder yaml GitSettings model class

    :ivar bool submodules: Whether to fetch submodules
    :ivar bool recursive: Whether to fetch submodules recursively
    :ivar bool lfs: Whether to set up lfs hooks and pull files
    :ivar bool depth: Depth to clone git repositories
    :ivar Optional[GitConfig] config: Custom git config values to set
    """

    def __init__(self):
        """Source __init__"""

        self.submodules: bool = False
        self.recursive: bool = False
        self.lfs: bool = False
        self.depth: Optional[int] = None
        self.config: Optional[GitConfig] = None

    @classmethod
    def combine_settings(cls, project: Project, section: Optional[Section],
                         defaults: Optional[Defaults]) -> 'ResolvedGitSettings':
        """Create instance updated with overrides from given GitSettings

        :param Project project: Project data model
        :param Optional[Section] section: Section data model
        :param Optional[Defaults] defaults: Defaults data model
        :return: Combined git settings
        """

        git_settings: ResolvedGitSettings = ResolvedGitSettings()

        has_defaults_git = defaults is not None and defaults.git_settings is not None
        if has_defaults_git:
            git_settings._update(defaults.git_settings)

        has_section_defaults = section is not None and section.defaults is not None
        has_section_defaults_git = has_section_defaults and section.defaults.git_settings is not None
        if has_section_defaults_git:
            git_settings._update(section.defaults.git_settings)

        has_git = project.git_settings is not None
        if has_git:
            git_settings._update(project.git_settings)

        return git_settings

    def _clean_config(self) -> None:
        """Remove any null value entries from config"""

        if self.config is None:
            return

        new_config = copy.deepcopy(self.config)
        for (k, v) in self.config.items():
            if v is None:
                del new_config[k]
        self.config = new_config

    def get_processed_config(self) -> Optional[Dict[str, str]]:
        """Return version of config converted to strings

        :return: Config processed to create strings
        :raise ClowderGitError:
        """

        if self.config is None:
            return None

        config: Dict[str, str] = {}
        for key, value in self.config.items():
            if isinstance(self.config[key], bool):
                config[key] = str(value).lower()
            elif isinstance(self.config[key], int) or isinstance(self.config[key], float):
                config[key] = str(value)
            elif isinstance(self.config[key], str):
                config[key] = value
            elif self.config[key] is None:
                pass
            else:
                raise Exception(f"Invalid git config value - {key}: {value}")
        return config

    def _update(self, git_settings: GitSettings) -> None:
        """Update with overrides from given GitSettings

        :return: Config processed to create strings
        :raise UnknownArgumentError:
        :raise UnknownTypeError:
        """

        if git_settings.submodules is not None:
            submodules = copy.deepcopy(git_settings.submodules)
            if isinstance(submodules, bool):
                self.submodules = submodules
                self.recursive = False
            elif isinstance(submodules, str):
                if submodules == "recursive":
                    self.submodules = True
                    self.recursive = True
                else:
                    raise UnknownArgumentError(f"Unknown submodules argument: {submodules}")
            else:
                raise UnknownTypeError("Unknown submodules type")
        if git_settings.lfs is not None:
            self.lfs = copy.deepcopy(git_settings.lfs)
        if git_settings.depth is not None:
            self.depth = copy.deepcopy(git_settings.depth)
        if git_settings.config is not None:
            if self.config is None:
                self.config = copy.deepcopy(git_settings.config)
            else:
                for (k, v) in git_settings.config.items():
                    self.config[k] = v

        self._clean_config()
