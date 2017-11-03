# -*- coding: utf-8 -*-
"""Various decorator utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.cli.globals import CLOWDER_REPO
from clowder.util.connectivity import is_offline


def clowder_required(func):
    """If no clowder repo, print clowder not found message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        _validate_clowder_repo_exists(CLOWDER_REPO)
        return func(*args, **kwargs)

    return wrapper


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached(print_output=True):
            return
        return func(*args, **kwargs)

    return wrapper


def project_repo_exists(func):
    """If no git repo exists, print message and return"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if not os.path.isdir(os.path.join(instance.full_path(), '.git')):
            cprint(" - Project repo is missing", 'red')
            return
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        CLOWDER_REPO.print_status()
        return func(*args, **kwargs)

    return wrapper


def print_clowder_repo_status_fetch(func):
    """Print clowder repo status"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        CLOWDER_REPO.print_status(fetch=True)
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
        _validate_clowder_repo_exists(instance.clowder_repo)
        if instance.invalid_yaml:
            print(fmt.invalid_yaml_error())
            print(fmt.error(instance.error))
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def _validate_clowder_repo_exists(repo):
    """If clowder repo doesn't exist, print message and exit

    :param ClowderRepo repo: Repo to check
    """

    if repo is None:
        cprint(' - No clowder found in the current directory\n', 'red')
        sys.exit(1)
