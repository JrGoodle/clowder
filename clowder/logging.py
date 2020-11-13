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

    def error(self, message: Optional[str], error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.ERROR:
            self._log(logging.ERROR, message, error)

    def debug(self, message: Optional[str] = None, error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.DEBUG:
            self._log(logging.DEBUG, message, error)

    def verbose(self, message: Optional[str], error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= self.VERBOSE:
            self._log(self.VERBOSE, message, error)

    def _log(self, level: int, message: Optional[str], error: Optional[BaseException] = None) -> None:  # noqa
        if message is not None:
            CONSOLE.log(message.strip())
        if error is not None:
            CONSOLE.log(CONSOLE.pretty_traceback)


LOG: Log = Log()
