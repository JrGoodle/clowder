"""Decorators

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path

import clowder.clowder_repo as clowder_repo
import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.console import CONSOLE
from clowder.error import ClowderError, ClowderErrorType
from clowder.environment import ENVIRONMENT


def clowder_repo_required(func):
    """If no clowder repo exists, print clowder repo not found message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_repo_existing_file_error is not None:
            raise ENVIRONMENT.clowder_repo_existing_file_error
        if ENVIRONMENT.clowder_repo_dir is None:
            message = f"No {fmt.path(Path('.clowder'))} directory found"
            raise ClowderError(ClowderErrorType.MISSING_CLOWDER_REPO, message)

        return func(*args, **kwargs)

    return wrapper


def clowder_git_repo_required(func):
    """If no clowder git repo exists, print clowder git repo not found message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir is None:
            message = f"No {fmt.path(Path('.clowder'))} git repository found"
            raise ClowderError(ClowderErrorType.MISSING_CLOWDER_GIT_REPO, message)
        return func(*args, **kwargs)

    return wrapper


def print_clowder_name(func):
    """Print clowder name"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if CLOWDER_CONTROLLER.name is not None:
            CONSOLE.stdout(f'{fmt.clowder_name(CLOWDER_CONTROLLER.name)}\n')
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

        if ENVIRONMENT.ambiguous_clowder_yaml_error is not None:
            raise ENVIRONMENT.ambiguous_clowder_yaml_error
        if ENVIRONMENT.clowder_yaml_missing_source_error is not None:
            raise ENVIRONMENT.clowder_yaml_missing_source_error
        if CLOWDER_CONTROLLER.error is not None:
            raise CLOWDER_CONTROLLER.error
        return func(*args, **kwargs)

    return wrapper
