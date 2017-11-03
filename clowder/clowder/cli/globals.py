# -*- coding: utf-8 -*-
"""Clowder command line global variables

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from clowder.clowder_controller import ClowderController
from clowder.clowder_repo import ClowderRepo


CLOWDER_CONTROLLER = ClowderController(os.getcwd())
CLOWDER_REPO = ClowderRepo(os.getcwd())
