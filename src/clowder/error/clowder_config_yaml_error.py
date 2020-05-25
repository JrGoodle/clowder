# -*- coding: utf-8 -*-
"""Clowder config yaml exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import IntEnum, unique


# Reserve range 41-70
# For reserved error codes see: http://tldp.org/LDP/abs/html/exitcodes.html
@unique
class ClowderConfigYAMLErrorType(IntEnum):
    UNKNOWN = 31
    EMPTY_FILE = 32
    OPEN_FILE = 33
    MISSING_PROJECT = 34
    INVALID_CLOWDER_PATH = 35


class ClowderConfigYAMLError(Exception):
    """Clowder config yaml error type"""

    def __init__(self, message: str, code: int):
        """ClowderConfigYAMLError __init__

        :param str message: Error message
        :param int code: Exit code
        """

        super(Exception, self).__init__()
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


# Reserve range 31-60
# For reserved error codes see: http://tldp.org/LDP/abs/html/exitcodes.html
@unique
class ClowderConfigYAMLErrorType(IntEnum):
    UNKNOWN = 31
    EMPTY_FILE = 32
    OPEN_FILE = 33
    JSONSCHEMA_VALIDATION_FAILED = 34
    MISSING_PROJECT = 35
    INVALID_CLOWDER_PATH = 36
