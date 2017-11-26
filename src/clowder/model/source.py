# -*- coding: utf-8 -*-
"""Representation of clowder.yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class Source(object):
    """clowder.yaml Source model class

    :ivar str name: Source name
    :ivar str url: Source url
    """

    def __init__(self, source):
        """Source __init__

        :param dict source: Parsed YAML python object for source
        """

        self.name = source['name']
        self.url = source['url']

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'name': self.name, 'url': self.url}
