# -*- coding: utf-8 -*-
"""clowder.yaml validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import CLOWDER_REPO
from clowder.error.clowder_exit import ClowderExit


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
            _invalid_yaml_error(CLOWDER_REPO.error)
        if CLOWDER_CONTROLLER.error:
            _invalid_yaml_error(CLOWDER_CONTROLLER.error)
        return func(*args, **kwargs)

    return wrapper


def _invalid_yaml_error(error):
    """Print invalid yaml message and raise exception

    :param Exception error: Exception raised during yaml validation/loading
    :raise ClowderExit:
    """

    print(fmt.invalid_yaml_error())
    print(fmt.error(error))
    raise ClowderExit(42)


def _validate_clowder_repo_exists():
    """If clowder repo doesn't exist, print message and exit

    :raise ClowderExit:
    """

    if not os.path.isdir(CLOWDER_REPO.clowder_path):
        cprint(' - No .clowder found in the current directory\n', 'red')
        raise ClowderExit(1)
