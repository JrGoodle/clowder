# -*- coding: utf-8 -*-
"""Source controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Dict

from clowder.model import Source


class SourceController(object):
    """Class encapsulating project information from clowder yaml for controlling clowder

    :ivar Dict[Source] sources: Dict of all Sources
    """

    def __init__(self):
        """SourceController __init__"""

        self.sources: Dict[Source] = {}

    def add_source(self, source: Source):
        """Returns all project names containing forks

        :param Source source: Source to add
        """

        # TODO: Implement

    def get_source(self, name: str) -> Source:
        """Returns Source by name

        :param str name: Source name to return
        :return: Source with supplied name
        :rtype: Source
        """

        # TODO: Implement


SOURCE_CONTROLLER: SourceController = SourceController()
