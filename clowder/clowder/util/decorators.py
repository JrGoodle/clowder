# -*- coding: utf-8 -*-
"""Various decorator utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

from termcolor import cprint

import clowder.util.formatting as fmt
from clowder.util.connectivity import is_offline


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


def network_connection_required(func):
    """If no network connection, print offline message and exit"""

    def wrapper(*args, **kwargs):
        """Wrapper"""

        if is_offline():
            print(fmt.offline_error())
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper
