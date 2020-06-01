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
logger = logging.getLogger("CLOWDER")

if PRINT_DEBUG_OUTPUT:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)


def LOG_DEBUG(message: str, exception: Optional[BaseException] = None) -> None: # noqa
    if PRINT_DEBUG_OUTPUT:
        print('=================== CLOWDER DEBUG - BEGIN ===================')
        logger.log(logging.DEBUG, f" {message}")
        if exception is not None:
            # TODO: Format the output for clowder debug
            traceback.print_exc()
        print('==================== CLOWDER DEBUG - END ====================')
