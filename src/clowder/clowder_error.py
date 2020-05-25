# -*- coding: utf-8 -*-
"""Clowder general exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import IntEnum, unique
from typing import Optional


@unique
class ClowderErrorType(IntEnum):
    UNKNOWN = 3


class ClowderError(Exception):
    """Clowder error type"""

    def __init__(self, error_type: ClowderErrorType, message: Optional[str] = None):
        """ClowderError __init__

        :param ClowderErrorType error_type: Clowder error type
        :param Optional[str] message: Error message
        """

        super().__init__(error_type)
        self.message = message
        self.error_type = error_type

    def __str__(self):
        return self.message if isinstance(self.message, str) else super().__str__()


# FIXME: Update values to match range
# Reserve range 11-40
# For reserved error codes see: http://tldp.org/LDP/abs/html/exitcodes.html
@unique
class ClowderYAMLErrorType(ClowderErrorType):
    UNKNOWN = 9
    MISSING_REPO = 10
    MISSING_YAML = 11
    EMPTY_FILE = 12
    OPEN_FILE = 13
    JSONSCHEMA_VALIDATION_FAILED = 14
    DUPLICATE_REMOTE_NAME = 15
    SOURCE_NOT_FOUND = 16
    DUPLICATE_PATH = 17
    

# Reserve range 41-70
# For reserved error codes see: http://tldp.org/LDP/abs/html/exitcodes.html
@unique
class ClowderConfigYAMLErrorType(ClowderErrorType):
    UNKNOWN = 31
    EMPTY_FILE = 32
    OPEN_FILE = 33
    JSONSCHEMA_VALIDATION_FAILED = 34
    MISSING_PROJECT = 35
    INVALID_CLOWDER_PATH = 36
