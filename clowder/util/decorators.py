"""Decorators

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.console import CONSOLE
from clowder.environment import ENVIRONMENT
from clowder.git.clowder_repo import ClowderRepo


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

        if ENVIRONMENT.clowder_repo_dir.is_dir():
            ClowderRepo(ENVIRONMENT.clowder_repo_dir).print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir:
            ClowderRepo(ENVIRONMENT.clowder_git_repo_dir).print_status(fetch=True)
        return func(*args, **kwargs)

    return wrapper
