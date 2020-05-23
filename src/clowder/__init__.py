# -*- coding: utf-8 -*-
"""clowder module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import logging
import os
from pathlib import Path
from typing import Optional


PRINT_DEBUG_OUTPUT = "CLOWDER_DEBUG" in os.environ
logging.basicConfig()
if PRINT_DEBUG_OUTPUT:
    logging.getLogger("CLOWDER DEBUG").setLevel(logging.DEBUG)
else:
    logging.getLogger("CLOWDER DEBUG").setLevel(logging.ERROR)
LOG_DEBUG = logging.getLogger("CLOWDER DEBUG")

CURRENT_DIR = Path.cwd()
CLOWDER_CONFIG_DIR = Path.home() / '.config' / 'clowder'
CLOWDER_CONFIG_YAML = Path(CLOWDER_CONFIG_DIR) / 'clowder.config.yaml'
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
    clowder_yaml = CLOWDER_DIR / 'clowder.yaml'
    if clowder_yaml.is_symlink():
        CLOWDER_YAML = clowder_yaml

    clowder_versions = CLOWDER_REPO_DIR / 'versions'
    if clowder_versions.is_dir():
        CLOWDER_REPO_VERSIONS_DIR = clowder_versions
