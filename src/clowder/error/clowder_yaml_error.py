# -*- coding: utf-8 -*-
"""Clowder yaml exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import IntEnum, unique


class ClowderYAMLError(Exception):
    """Clowder yaml error type"""

    def __init__(self, message: str, code: int):
        """ClowderExit __init__

        :param str message: Error message
        :param int code: Exit code
        """

        super(Exception, self).__init__()
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


@unique
class ClowderYAMLYErrorType(IntEnum):
    UNKNOWN = 99
    REMOTE_NAME = 101
    MISSING_ENTRY = 102
    UNKNOWN_ENTRY = 103
    MISSING_YAML = 104
    EMPTY_YAML = 106
    OPEN_FILE = 107
    INVALID_PROTOCOL = 108
    INVALID_REF = 109
    DEPTH = 111
    TYPE = 112
    MISSING_REPO = 113
    SOURCE_NOT_FOUND = 114
