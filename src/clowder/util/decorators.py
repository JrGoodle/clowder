# -*- coding: utf-8 -*-
"""Decorators

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from functools import wraps

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder import CLOWDER_REPO_DIR
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.error import ClowderExit, ClowderYAMLError, ClowderYAMLErrorType


def clowder_repo_required(func):
    """If no clowder repo, print clowder not found message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_name(func):
    """Print clowder name"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        print(fmt.clowder_name(f"{CLOWDER_CONTROLLER.name}\n"))
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        clowder_repo.print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        clowder_repo.print_status(fetch=True)
        return func(*args, **kwargs)

    return wrapper


def valid_clowder_yaml_required(func):
    """If clowder yaml file is invalid, print invalid yaml message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists()
        if CLOWDER_CONTROLLER.error:
            _invalid_yaml_error(CLOWDER_CONTROLLER.error)
        return func(*args, **kwargs)

    return wrapper


def _invalid_yaml_error(error: Exception):
    """Print invalid yaml message and raise exception

    :param Exception error: Exception raised during yaml validation/loading
    :raise ClowderExit:
    """

    print(fmt.error(error))
    if isinstance(error, ClowderYAMLError):
        raise ClowderExit(error.code)
    raise ClowderExit(ClowderYAMLErrorType.UNKNOWN)


def _validate_clowder_repo_exists():
    """If clowder repo doesn't exist, print message and exit

    :raise ClowderExit:
    """

    if CLOWDER_REPO_DIR is None:
        print(f"{fmt.ERROR} No '.clowder' directory found")
        raise ClowderExit(ClowderYAMLErrorType.MISSING_REPO)
