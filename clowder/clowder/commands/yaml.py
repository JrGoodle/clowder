# -*- coding: utf-8 -*-
"""Clowder yaml command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import sys

import clowder.util.formatting as fmt
from clowder.yaml.printing import print_yaml


def yaml(clowder, resolved):
    """Print clowder.yaml

    :param ClowderController clowder: ClowderController instance
    :param bool resolved: Print clowder.yaml with all values populated rather than the file contents
    """

    if resolved:
        print(fmt.yaml_string(clowder.get_yaml_resolved()))
    else:
        print_yaml(clowder.root_directory)
    sys.exit()  # exit early to prevent printing extra newline
