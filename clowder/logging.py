"""Clowder logging utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import logging
import os
from typing import Optional

from clowder.console import CONSOLE


PRINT_DEBUG_OUTPUT = "CLOWDER_DEBUG" in os.environ


class Log:
    """clowder log class"""

    logger_name: str = 'CLOWDER'
    VERBOSE: int = 5

    def __init__(self):
        logging.basicConfig()
        logging.raiseExceptions = True
        logging.addLevelName(Log.VERBOSE, 'VERBOSE')
        self.logger = logging.getLogger(self.logger_name)

        self.level = logging.DEBUG
        # environment = os.environ
        # if PRINT_DEBUG_OUTPUT:
        #     self.level = logging.DEBUG
        # else:
        #     self.level = logging.ERROR

    @property
    def level(self) -> int:
        return self.logger.level

    @level.setter
    def level(self, level: int):
        self.logger.setLevel(level)

    def error(self, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.ERROR:
            self._log(logging.ERROR, message, exception)

    def debug(self, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.DEBUG:
            self._log(logging.DEBUG, message, exception)

    def verbose(self, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= self.VERBOSE:
            self._log(self.VERBOSE, message)

    def _log(self, level: int, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        separator = '='
        output = f' BEGIN {separator * 78}\n'
        output += f'{message.strip()}\n'
        if exception is not None:
            output += CONSOLE.pretty_traceback()
        output += f'{logging.getLevelName(level)}:{self.logger_name}: END {separator * 80}\n'
        CONSOLE.log(output)
        # self.logger.log(level, output)


LOG: Log = Log()
