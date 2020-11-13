"""Clowder error

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import IntEnum, unique
from typing import List, Union


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
    PRUNE_NO_BRANCHES = 25
    INVALID_GIT_PROTOCOL = 26
    PARALLEL_COMMAND_UNAVAILABLE = 27
    INVALID_GIT_CONFIG_VALUE = 28
    INVALID_GIT_SETTINGS_INIT_PARAMETERS = 29
    CLOWDER_SYMLINK_SOURCE_MISSING = 30
    MISSING_CLOWDER_GIT_REPO = 35
    MISSING_CLOWDER_REPO = 36
    EXISTING_FILE_AT_SYMLINK_TARGET_PATH = 37
    FAILED_SYMLINK_FILE = 38
    SYMLINK_SOURCE_NOT_FOUND = 39
    CLOWDER_REPO_EXISTING_FILE = 70
    PARSER_CREATION_FAILED = 71
    PROJECT_NOT_FOUND = 72
    WRONG_SOURCE_TYPE = 73
    WRONG_UPSTREAM_TYPE = 74
    SOURCES_NOT_VALIDATED = 75
    SOURCES_ALREADY_VALIDATED = 76
    WRONG_GROUP_TYPE = 77
    WRONG_SUBMODULES_TYPE = 78

    OPEN_FILE = 45

    # Yaml errors
    YAML_UNKNOWN = 41
    YAML_MISSING_FILE = 42
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
    """

    def __init__(self, error_type: ClowderErrorType, messages: Union[str, List[str]]):
        """ClowderError __init__

        :param ClowderErrorType error_type: Clowder error type
        :param Union[str, List[str]] messages: Error message(s)
        """

        if isinstance(messages, str):
            self.messages: List[str] = [messages]
        else:
            self.messages: List[str] = messages
        self.error_type: ClowderErrorType = error_type

    def __str__(self):
        return "\n".join(self.messages)
