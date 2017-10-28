"""Decorators"""

import sys

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.git.project_repo import ProjectRepo
from clowder.util.connectivity import is_offline


def clowder_required(func):
    """If no clowder repo, print clowder not found message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.clowder_repo is None:
            cprint(' - No clowder found in the current directory\n', 'red')
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def initialize_skip_projects(func):
    """Initialize skip projects to empty list if necessary"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        if kwargs['skip'] is None:
            kwargs['skip'] = []
        return func(*args, **kwargs)

    return wrapper


def project_repo_exists(func):
    """If no git repo exists, print error message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not ProjectRepo.existing_git_repository(instance.full_path()):
            cprint(" - Project repo is missing", 'red')
            return
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        instance.clowder_repo.print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        instance.clowder_repo.print_status(fetch=True)
        return func(*args, **kwargs)

    return wrapper


def network_connection_required(func):
    """If no network connection, print offline message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def valid_clowder_yaml_required(func):
    """If clowder.yaml is invalid, print invalid yaml message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.invalid_yaml:
            print(fmt.invalid_yaml_error())
            print(fmt.error(instance.error))
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper
