# -*- coding: utf-8 -*-
"""Representation of clowder yaml source name

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class SourceName:
    """clowder yaml SourceName model class

    :ivar str name: Source name
    """

    def __init__(self, name: str):
        """Source __init__

        :param str name: Source name
        """

        self.name: str = name

    def __eq__(self, other):
        """Overrides the default implementation"""

        if isinstance(other, SourceName):
            return self.name == other.name
        return False

    def __hash__(self):
        """Overrides the default implementation"""

        return hash(self.name)

    def get_yaml(self) -> str:
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: str
        """

        return self.name
