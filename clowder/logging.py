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
            self.level = logging.DEBUG
        else:
            self.level = logging.ERROR

    @property
    def level(self) -> int:
        return self.logger.level

    @level.setter
    def level(self, level: int):
        self.logger.setLevel(level)

    def debug(self, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if PRINT_DEBUG_OUTPUT:
            separator = '='
            output = f' BEGIN {separator * 78}\n'
            output += f'{message.strip()}\n'
            if exception is not None:
                output += traceback.format_exc()
            output += f'DEBUG:{self.logger_name}: END {separator * 80}\n'
            self.logger.log(logging.DEBUG, output)

    def verbose(self, message: str, exception: Optional[BaseException] = None) -> None:  # noqa
        if PRINT_DEBUG_OUTPUT:
            separator = '='
            output = f' BEGIN {separator * 78}\n'
            output += f'{message.strip()}\n'
            if exception is not None:
                output += traceback.format_exc()
            output += f'INFO:{self.logger_name}: END {separator * 80}\n'
            self.logger.log(self.VERBOSE, output)


LOG: Log = Log()
