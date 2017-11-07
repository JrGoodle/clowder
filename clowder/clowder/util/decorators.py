# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import CLOWDER_REPO


def clowder_required(func):
    """If no clowder repo, print clowder not found message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        return func(*args, **kwargs)

    return wrapper


def valid_clowder_yaml_required(func):
    """If clowder.yaml is invalid, print invalid yaml message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        if CLOWDER_REPO.error:
            print(fmt.invalid_yaml_error())
            print(fmt.error(CLOWDER_REPO.error))
            sys.exit(42)
        if CLOWDER_CONTROLLER.error:
            print(fmt.invalid_yaml_error())
            print(fmt.error(CLOWDER_CONTROLLER.error))
            sys.exit(42)
        return func(*args, **kwargs)

    return wrapper


def _validate_clowder_repo_exists():
    """If clowder repo doesn't exist, print message and exit"""

    if not os.path.isdir(CLOWDER_REPO.clowder_path):
        cprint(' - No .clowder found in the current directory\n', 'red')
        sys.exit(1)
