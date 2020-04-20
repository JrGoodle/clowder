# -*- coding: utf-8 -*-
"""Representation of clowder.yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class Source(object):
    """clowder.yaml Source model class

    :ivar str name: Source name
    :ivar str url: Source url
    """

    def __init__(self, source, defaults):
        """Source __init__

        :param dict source: Parsed YAML python object for source
        :param Defaults defaults: Defaults instance
        """

        self.name = source['name']
        self.url = source['url']
        self.protocol = source.get('protocol', defaults.protocol)

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'name': self.name, 'url': self.url, 'protocol': self.protocol}
