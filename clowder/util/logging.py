"""Clowder logging utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import logging
import os
from typing import Optional

from clowder.console import CONSOLE


LOG_LEVEL: Optional[str] = os.environ.get("CLOWDER_LOG", None)
CLOWDER_DEBUG: bool = 'CLOWDER_DEBUG' in os.environ


class Log:
    """clowder log class"""

    logger_name: str = 'CLOWDER'
    VERBOSE: int = 5
    DEBUG: int = logging.DEBUG
    ERROR: int = logging.ERROR

    def __init__(self):
        logging.basicConfig()
        logging.raiseExceptions = True
        logging.addLevelName(Log.VERBOSE, 'VERBOSE')
        self.logger = logging.getLogger(self.logger_name)

        if LOG_LEVEL == 'VERBOSE':
            self.level = self.VERBOSE
        elif LOG_LEVEL == 'DEBUG' or CLOWDER_DEBUG:
            self.level = self.DEBUG
        else:
            self.level = self.ERROR

    @property
    def level(self) -> int:
        return self.logger.level

    @level.setter
    def level(self, level: int):
        self.logger.setLevel(level)

    def error(self, message: Optional[str] = None, error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.ERROR:
            self._log(logging.ERROR, message, error)

    def debug(self, message: Optional[str] = None, error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= logging.DEBUG:
            self._log(logging.DEBUG, message, error)

    def verbose(self, message: Optional[str] = None, error: Optional[BaseException] = None) -> None:  # noqa
        if self.logger.level <= self.VERBOSE:
            self._log(self.VERBOSE, message, error)

    def _log(self, level: int, message: Optional[str], error: Optional[BaseException] = None) -> None:  # noqa
        if message is not None:
            CONSOLE.stderr(message.strip())
        if error is not None:
            CONSOLE.print_exception()


LOG: Log = Log()
