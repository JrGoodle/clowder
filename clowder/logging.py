"""Clowder logging utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import logging
import os
from typing import Optional

from clowder.console import CONSOLE


LOG_LEVEL = os.environ.get("CLOWDER_LOG", None)


class Log:
    """clowder log class"""

    logger_name: str = 'CLOWDER'
    VERBOSE: int = 5

    def __init__(self):
        logging.basicConfig()
        logging.raiseExceptions = True
        logging.addLevelName(Log.VERBOSE, 'VERBOSE')
        self.logger = logging.getLogger(self.logger_name)

        if LOG_LEVEL is None or LOG_LEVEL is 'VERBOSE':
            self.level = self.VERBOSE
        elif LOG_LEVEL is 'DEBUG':
            self.level = logging.DEBUG
        else:
            self.level = logging.ERROR

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
            CONSOLE.stderr(CONSOLE.pretty_traceback)


LOG: Log = Log()
