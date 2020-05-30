# -*- coding: utf-8 -*-
"""Clowder error

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import copy
from enum import IntEnum, unique
from typing import List, Optional, Union

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
    OPEN_FILE = 45
    MISSING_REPO = 42
    PRUNE_NO_BRANCHES = 25
    INVALID_GIT_PROTOCOL = 26
    PARALLEL_COMMAND_UNAVAILABLE = 27
    INVALID_GIT_CONFIG_VALUE = 28
    INVALID_GIT_SETTINGS_INIT_PARAMETERS = 29

    # Yaml errors
    YAML_UNKNOWN = 41
    YAML_MISSING_FILE = 43
    YAML_EMPTY_FILE = 44
    YAML_JSONSCHEMA_VALIDATION_FAILED = 46

    # Clowder yaml errors
    CLOWDER_YAML_UNKNOWN = 40
    CLOWDER_YAML_DUPLICATE_REMOTE_NAME = 47
    CLOWDER_YAML_SOURCE_NOT_FOUND = 48
    CLOWDER_YAML_DUPLICATE_PATH = 49

    # Config yaml errors
    CONFIG_YAML_UNKNOWN = 64
    CONFIG_YAML_UNKNOWN_PROJECT = 65
    CONFIG_YAML_INVALID_CLOWDER_PATH = 66


class ClowderError(Exception):
    """Clowder error type

    :ivar ClowderErrorType error_type: Clowder error type
    :ivar List[str] messages: List of messages to print
    :ivar Tuple[Group, ...] groups: List of all Groups
    """

    def __init__(self, error_type: ClowderErrorType, messages: Union[str, List[str]],
                 error: Optional[Exception] = None, exit_code: Optional[int] = None):
        """ClowderError __init__

        :param ClowderErrorType error_type: Clowder error type
        :param Union[str, List[str]] messages: Error message
        :param Optional[Exception] error: Optional error to print
        :param Optional[int] exit_code: Custom error code
        """

        if isinstance(messages, str):
            self.messages = [messages]
        else:
            self.messages = messages
        self.error_type = error_type
        self.error = error
        self.exit_code = exit_code

    def __str__(self):
        messages = copy.deepcopy(self.messages)
        if self.error is not None:
            messages.append(fmt.error(self.error))
        return "\n".join(messages)
