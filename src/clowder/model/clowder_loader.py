# -*- coding: utf-8 -*-
"""Representation of clowder yaml loader

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path

import clowder.util.formatting as fmt
from clowder.environment import ENVIRONMENT
from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG

from .defaults import Defaults
from .group import Group
from .project import Project
from .source import Source, DEFAULT_SOURCES


class ClowderLoader:
    """clowder yaml loader class

    :ivar str name: Name of clowder
    :ivar Optional[Defaults] defaults: Name of clowder
    :ivar Optional[List[Source]] sources: Sources
    :ivar Clowder clowder: Clowder model
    """

    def __init__(self, yaml: dict):
        """Upstream __init__

        :param dict yaml: Parsed yaml dict
        """

        self._load_clowder_yaml(yaml)

    def _load_clowder_yaml(self, yaml: dict) -> None:
        """Load clowder yaml file

        :param dict yaml: Parsed yaml dict
        """
        try:
            self.name = yaml['name']
            self.defaults = Defaults(yaml.get('defaults', {}))

            # Load sources
            self.sources = [Source(name, s, self.defaults, True) for name, s in yaml.get('sources', {}).items()]
            # Load default sources if not already specified
            for name, ds in DEFAULT_SOURCES.items():
                if not any([s.name == name for s in self.sources]):
                    self.sources.append(Source(name, ds, self.defaults, False))
            self.sources = tuple(sorted(self.sources, key=lambda source: source.name))
            # Check for unknown sources
            if not any([s.name == self.defaults.source for s in self.sources]):
                message = fmt.error_source_default_not_found(self.defaults.source, ENVIRONMENT.clowder_yaml)
                raise ClowderError(ClowderErrorType.CLOWDER_YAML_SOURCE_NOT_FOUND, message)

            # Load groups
            groups = [Group(n, g, self.defaults, self.sources) for n, g in yaml.get('groups', {}).items()]
            self.groups = tuple(sorted(groups, key=lambda group: group.name))

            # Load projects
            non_group_projects = [Project(p, self.defaults, self.sources) for p in yaml.get('projects', [])]
            self.non_group_projects = tuple(sorted(non_group_projects, key=lambda project: project.name))
            all_projects = non_group_projects + [p for g in groups for p in g.projects]
            self.projects = tuple(sorted(all_projects, key=lambda project: project.name))

            # Validate projects don't share share directories
            paths = [str(p.path.resolve()) for p in self.projects]
            duplicate = fmt.check_for_duplicates(paths)
            if duplicate is not None:
                message = fmt.error_duplicate_project_path(Path(duplicate), ENVIRONMENT.clowder_yaml)
                raise ClowderError(ClowderErrorType.CLOWDER_YAML_DUPLICATE_PATH, message)

        except (AttributeError, KeyError, TypeError) as err:
            LOG_DEBUG('Failed to load clowder yaml', err)
