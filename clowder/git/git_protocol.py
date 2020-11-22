"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique

from clowder.util.error import UnknownTypeError
from clowder.util.enum import AutoLowerName


@unique
class GitProtocol(AutoLowerName):
    SSH = auto()
    HTTPS = auto()

    def format_url(self, url: str, name: str) -> str:
        """Return formatted git url

        :param str url: Repo url
        :param str name: Repo name
        :return: Full git repo url for specified protocol
        :raise UnknownTypeError:
        """

        if self is GitProtocol.SSH:
            return f"git@{url}:{name}.git"
        elif self is GitProtocol.HTTPS:
            return f"https://{url}/{name}.git"
        else:
            raise UnknownTypeError('Invalid git protocol')
