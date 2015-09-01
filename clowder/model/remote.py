"""Model representation of clowder.yaml remote"""

class Remote(object):
    """Model class for clowder.yaml remote"""

    def __init__(self, remote):
        self.name = remote['name']
        self.url = remote['url']

    def get_url_prefix(self):
        """Return full remote url for project"""
        remote_url_prefix = None
        if self.url.startswith('https://'):
            remote_url_prefix = self.url + "/"
        elif self.url.startswith('ssh://'):
            remote_url_prefix = self.url[6:] + ":"
        return remote_url_prefix

    def get_yaml(self):
        """Return python object representation for saving yaml"""
        return {'name': self.name, 'url': self.url}
