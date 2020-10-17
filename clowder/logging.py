# -*- coding: utf-8 -*-
"""Clowder logging utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import logging
import os
import traceback
from typing import Optional


PRINT_DEBUG_OUTPUT = "CLOWDER_DEBUG" in os.environ

logging.basicConfig()
logging.raiseExceptions = True
logger_name: str = 'CLOWDER'
logger = logging.getLogger(logger_name)

if PRINT_DEBUG_OUTPUT:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)


def LOG_DEBUG(message: str, exception: Optional[BaseException] = None) -> None:  # noqa
    if PRINT_DEBUG_OUTPUT:
        separator = '='
        output = f' BEGIN {separator * 78}\n'
        output += f'{message.strip()}\n'
        if exception is not None:
            output += traceback.format_exc()
        output += f'DEBUG:{logger_name}: END {separator * 80}\n'
        logger.log(logging.DEBUG, output)
