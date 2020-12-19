"""Clowder git utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import wraps

from pygoodle.console import CONSOLE


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if instance.is_detached:
            CONSOLE.stdout(' - HEAD is detached')
            return
        return func(*args, **kwargs)

    return wrapper
