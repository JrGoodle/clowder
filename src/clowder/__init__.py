# -*- coding: utf-8 -*-
"""clowder module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from clowder.error import ClowderError, ClowderErrorType
from clowder.logging import LOG_DEBUG
from clowder.util.formatting import error_ambiguous_clowder_yaml
from clowder.git.util import existing_git_repository


# Set up global paths #

CURRENT_DIR = Path.cwd()
CLOWDER_CONFIG_DIR = Path.home() / '.config' / 'clowder'
CLOWDER_CONFIG_YAML = CLOWDER_CONFIG_DIR / 'clowder.config.yml'
CLOWDER_DIR: Optional[Path] = None
CLOWDER_REPO_DIR: Optional[Path] = None
CLOWDER_REPO_VERSIONS_DIR: Optional[Path] = None
CLOWDER_YAML: Optional[Path] = None


def existing_clowder_repo(directory: Path) -> bool:
    """Check if directory is a clowder repository

    :param Path directory: Path to check
    :return: True, if it looks like it's a clowder repository
    :rtype: bool
    """

    return directory.is_dir() and existing_git_repository(directory)


# Walk up directory tree to find possible clowder repo (.clowder directory) and set global variable
path = Path.cwd()
while str(path) != path.root:
    clowder_repo_dir = path / '.clowder'
    if existing_clowder_repo(clowder_repo_dir):
        CLOWDER_DIR = path
        CLOWDER_REPO_DIR = clowder_repo_dir
        break
    path = path.parent


# If clowder repo exists, try to set other global path variables
if CLOWDER_REPO_DIR is not None:
    clowder_yml = CLOWDER_DIR / 'clowder.yml'
    clowder_yaml = CLOWDER_DIR / 'clowder.yaml'
    if clowder_yml.is_symlink() and clowder_yaml.is_symlink():
        print(error_ambiguous_clowder_yaml())
        try:
            raise ClowderError(ClowderErrorType.AMBIGUOUS_CLOWDER_YAML, error_ambiguous_clowder_yaml())
        except ClowderError as err:
            LOG_DEBUG('Ambigiuous clowder file', err)
            print()
            exit(err.error_type.value)
    if clowder_yml.is_symlink():
        # TODO: Check whether symlink source exists
        CLOWDER_YAML = clowder_yml
    elif clowder_yaml.is_symlink():
        # TODO: Check whether symlink source exists
        CLOWDER_YAML = clowder_yaml

    clowder_versions = CLOWDER_REPO_DIR / 'versions'
    if clowder_versions.is_dir():
        CLOWDER_REPO_VERSIONS_DIR = clowder_versions
