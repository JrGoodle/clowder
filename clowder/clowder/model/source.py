# -*- coding: utf-8 -*-
"""Representation of clowder.yaml source

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class Source(object):
    """clowder.yaml source class"""

    def __init__(self, source):
        self.name = source['name']
        self.url = source['url']

    def get_url_prefix(self):
        """Return full remote url prefix for project

        :return: Remote URL prefix
        :rtype: str
        """

        source_url_prefix = None
        if self.url.startswith('https://'):
            source_url_prefix = self.url + "/"
        elif self.url.startswith('ssh://'):
            source_url_prefix = self.url[6:] + ":"
        return source_url_prefix

    def get_yaml(self):
        """Return python object representation for saving yaml

        :return: YAML python object
        :rtype: dict
        """

        return {'name': self.name, 'url': self.url}
