# -*- coding: utf-8 -*-
"""clowder module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import pkg_resources
from typing import Optional


CLOWDER_SCHEMA = pkg_resources.resource_string(__name__, "clowder.schema.json")


CURRENT_DIR: str = os.getcwd()
CLOWDER_DIR: Optional[str] = None
CLOWDER_REPO_DIR: Optional[str] = None
CLOWDER_REPO_VERSIONS_DIR: Optional[str] = None
CLOWDER_YAML: Optional[str] = None


temp_dir = CURRENT_DIR
old_dir = None
# Walk up directory tree to find possible clowder repo (.clowder directory) and set global variable
while old_dir != temp_dir:
    old_dir = temp_dir
    clowder_repo_dir = os.path.join(temp_dir, '.clowder')
    if os.path.exists(clowder_repo_dir) and os.path.isdir(clowder_repo_dir):
        CLOWDER_DIR = temp_dir
        CLOWDER_REPO_DIR = clowder_repo_dir
        break
    else:
        temp_dir = os.path.dirname(temp_dir)

# If clowder repo exists, try to set other global path variables
if CLOWDER_REPO_DIR is not None:
    clowder_yaml = os.path.join(CLOWDER_DIR, 'clowder.yaml')
    if os.path.islink(clowder_yaml):
        CLOWDER_YAML = clowder_yaml

    clowder_versions = os.path.join(CLOWDER_REPO_DIR, 'versions')
    if os.path.isdir(clowder_versions):
        CLOWDER_REPO_VERSIONS_DIR = clowder_versions

