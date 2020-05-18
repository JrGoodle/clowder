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
class ClowderYAMLErrorType(IntEnum):
    UNKNOWN = 9
    MISSING_REPO = 10
    MISSING_YAML = 11
    EMPTY_FILE = 12
    OPEN_FILE = 13
    JSONSCHEMA_VALIDATION_FAILED = 14
    DUPLICATE_REMOTE_NAME = 15
    SOURCE_NOT_FOUND = 16
    DUPLICATE_PATH = 17
