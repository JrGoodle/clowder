# -*- coding: utf-8 -*-
"""Clowder general exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import IntEnum, unique
from typing import Optional

import clowder.util.formatting as fmt


# Reserve range 3-30
# For reserved error codes see: http://tldp.org/LDP/abs/html/exitcodes.html
@unique
class ClowderErrorType(IntEnum):
    UNKNOWN = 3
    USER_INTERRUPT = 4
    AMBIGUOUS_CLOWDER_YAML = 5
    GIT_ERROR = 6
    INVALID_PROJECT_STATUS = 7
    DUPLICATE_SAVED_VERSIONS = 8
    FAILED_INIT = 9
    FAILED_EXECUTE_COMMAND = 10
    FAILED_YAML_DUMP = 11
    FAILED_REMOVE_FILE = 12
    FILE_EXISTS = 13
    FAILED_SAVE_FILE = 14
    FAILED_OPEN_FILE = 15
    PARALLEL_COMMAND_FAILED = 16
    FAILED_REMOVE_DIRECTORY = 17
    FAILED_CREATE_DIRECTORY = 18
    DIRECTORY_EXISTS = 19
    OFFLINE = 20
    UNKNOWN_CONFIG_TYPE = 21
    CLOWDER_ALREADY_INITIALIZED = 22
    SAVE_DEFAULT_VERSION = 23
    VERSION_ALREADY_EXISTS = 24


class ClowderError(Exception):
    """Clowder error type"""

    def __init__(self, error_type: ClowderErrorType, message: str, error: Optional[Exception] = None):
        """ClowderError __init__

        :param ClowderErrorType error_type: Clowder error type
        :param str message: Error message
        :param Optional[Exception] error: Optional error to print
        """

        super().__init__(error_type)
        self.message = message
        self.error_type = error_type
        self.error = error

    def __str__(self):
        if self.error is not None:
            return f"{self.message}\n{fmt.error(self.error)}"
        return self.message


# FIXME: Update values to match range
# Reserve range 41-60
@unique
class ClowderYAMLErrorType(ClowderErrorType):
    UNKNOWN = 41
    MISSING_REPO = 42
    MISSING_YAML = 43
    EMPTY_FILE = 44
    OPEN_FILE = 45
    JSONSCHEMA_VALIDATION_FAILED = 46
    DUPLICATE_REMOTE_NAME = 47
    SOURCE_NOT_FOUND = 48
    DUPLICATE_PATH = 49


# Reserve range 61-80
@unique
class ClowderConfigYAMLErrorType(ClowderErrorType):
    UNKNOWN = 61
    EMPTY_FILE = 62
    OPEN_FILE = 63
    JSONSCHEMA_VALIDATION_FAILED = 64
    UNKNOWN_PROJECT = 65
    INVALID_CLOWDER_PATH = 66
