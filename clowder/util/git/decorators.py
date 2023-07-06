"""git constants"""

from functools import wraps
from typing import Callable, Union

from pygoodle.console import CONSOLE
from pygoodle.git.offline import GitOffline
from pygoodle.git.log import GIT_LOG


def output_msg(message: Union[Callable, str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(message, Callable):
                instance = args[0]
                msg: str = message(instance)
            else:
                msg: str = str(message)
            CONSOLE.stdout(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def error_msg(message: Union[Callable, str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(message, Callable):
                instance = args[0]
                msg: str = message(instance)
            else:
                msg: str = str(message)
            try:
                return func(*args, **kwargs)
            except Exception:
                GIT_LOG.error(msg)
                raise
        return wrapper
    return decorator


def not_detached(func):
    """If HEAD is detached, print error message and exit"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        instance = args[0]
        if GitOffline.is_detached(instance.path):
            CONSOLE.stdout(' - HEAD is detached')
            raise Exception('Detached HEAD')
        return func(*args, **kwargs)

    return wrapper
