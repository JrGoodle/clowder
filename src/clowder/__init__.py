# -*- coding: utf-8 -*-
"""clowder module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import logging
import os
import traceback
from pathlib import Path
from typing import Optional

from clowder.error import ClowderExit
from clowder.util.formatting import ERROR

# Set up logging #

PRINT_DEBUG_OUTPUT = "CLOWDER_DEBUG" in os.environ
logging.basicConfig()
logging.raiseExceptions = True
logger = logging.getLogger("CLOWDER")
if PRINT_DEBUG_OUTPUT:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)


def LOG_DEBUG(message: str, exception: Optional[Exception] = None): # noqa
    if PRINT_DEBUG_OUTPUT:
        logger.log(logging.DEBUG, f" {message}")
        if exception is not None:
            logger.log(logging.DEBUG, str(exception))
            # TODO: Format the output for clowder debug
            traceback.print_exc()


# Set up global paths #

CURRENT_DIR = Path.cwd()
CLOWDER_CONFIG_DIR = Path.home() / '.config' / 'clowder'
CLOWDER_CONFIG_YAML = CLOWDER_CONFIG_DIR / 'clowder.config.yml'
CLOWDER_DIR: Optional[Path] = None
CLOWDER_REPO_DIR: Optional[Path] = None
CLOWDER_REPO_VERSIONS_DIR: Optional[Path] = None
CLOWDER_YAML: Optional[Path] = None


# Walk up directory tree to find possible clowder repo (.clowder directory) and set global variable
path = Path.cwd()
while str(path) != path.root:
    clowder_repo_dir = path / '.clowder'
    if clowder_repo_dir.is_dir():
        CLOWDER_DIR = path
        CLOWDER_REPO_DIR = clowder_repo_dir
        break
    else:
        path = path.parent


# If clowder repo exists, try to set other global path variables
if CLOWDER_REPO_DIR is not None:
    clowder_yml = CLOWDER_DIR / 'clowder.yml'
    clowder_yaml = CLOWDER_DIR / 'clowder.yaml'
    if clowder_yml.is_symlink() and clowder_yaml.is_symlink():
        print(f"\n{ERROR} Found clowder.yml and clowder.yaml files in same directory\n")
        try:
            raise ClowderExit(1)
        except ClowderExit as err:
            LOG_DEBUG('Ambigiuous clowder file', err)
            exit(err.code)
    if clowder_yml.is_symlink():
        CLOWDER_YAML = clowder_yml
    elif clowder_yaml.is_symlink():
        CLOWDER_YAML = clowder_yaml

    clowder_versions = CLOWDER_REPO_DIR / 'versions'
    if clowder_versions.is_dir():
        CLOWDER_REPO_VERSIONS_DIR = clowder_versions
