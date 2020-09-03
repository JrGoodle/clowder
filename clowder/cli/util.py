# -*- coding: utf-8 -*-
"""Clowder model utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import argparse

from typing import List, Tuple, Union


Parser = Union[argparse.ArgumentParser, argparse._MutuallyExclusiveGroup, argparse._ArgumentGroup] # noqa
Arguments = List[Tuple[list, dict]]


def add_parser_arguments(parser: Parser, arguments: Arguments) -> None:
    """Add arguments to parser

    :param Parser parser: Parser to add arguments to
    :param Arguments arguments: Arguments to add to parser
    """

    for argument in arguments:
        parser.add_argument(*argument[0], **argument[1])
