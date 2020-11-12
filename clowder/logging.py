"""Clowder logging utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

import logging
import os
import traceback
from typing import Optional


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

        if PRINT_DEBUG_OUTPUT:
            self.level = logging.ERROR
        else:
            self.level = logging.ERROR

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
            self._log(self.VERBOSE, message, exception)

    def _log(self, level: int, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if PRINT_DEBUG_OUTPUT:
            separator = '='
            output = f' BEGIN {separator * 78}\n'
            output += f'{message.strip()}\n'
            if exception is not None:
                output += traceback.format_exc()
            output += f'{logging.getLevelName(level)}:{self.logger_name}: END {separator * 80}\n'
            # https://stackoverflow.com/a/57859075
            import contextlib, io

            # f = io.StringIO()
            # with contextlib.redirect_stdout(f):
            #     module1.test()
            # output = f.getvalue()
            self.logger.log(level, output)


LOG: Log = Log()
