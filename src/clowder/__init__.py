# -*- coding: utf-8 -*-
"""Clowder module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import pkg_resources


ROOT_DIR = os.getcwd()

CLOWDER_SCHEMA = pkg_resources.resource_string(__name__, "clowder.schema.json")
