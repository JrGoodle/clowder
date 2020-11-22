"""Decorators

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps
from pathlib import Path

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.console import CONSOLE
from clowder.error import MissingClowderGitRepo, MissingClowderRepo
from clowder.environment import ENVIRONMENT
from clowder.git_project.clowder_repo import ClowderRepo


def clowder_repo_required(func):
    """If no clowder repo exists, print clowder repo not found message and exit

    :raise ExistingFileError:
    :raise MissingClowderGitRepo:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.existing_clowder_repo_file_error is not None:
            raise ENVIRONMENT.existing_clowder_repo_file_error
        if ENVIRONMENT.clowder_repo_dir is None:
            raise MissingClowderRepo(f"No {fmt.path(Path('.clowder'))} directory found")

        return func(*args, **kwargs)

    return wrapper


def clowder_git_repo_required(func):
    """If no clowder git repo exists, print clowder git repo not found message and exit

    :raise MissingClowderGitRepo:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.clowder_git_repo_dir is None:
            raise MissingClowderGitRepo(f"No {fmt.path(Path('.clowder'))} git repository found")
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


def valid_clowder_yaml_required(func):
    """If clowder yaml file is invalid, print invalid yaml message and exit

    :raise AmbiguousYamlError:
    :raise MissingSourceError:
    :raise Exception:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        if ENVIRONMENT.ambiguous_yaml_error is not None:
            raise ENVIRONMENT.ambiguous_yaml_error
        if ENVIRONMENT.missing_source_error is not None:
            raise ENVIRONMENT.missing_source_error
        if CLOWDER_CONTROLLER.error is not None:
            raise CLOWDER_CONTROLLER.error
        return func(*args, **kwargs)

    return wrapper
