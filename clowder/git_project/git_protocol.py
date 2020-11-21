"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique

from clowder.error import *
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
        :raise ClowderError:
        """

        if self is GitProtocol.SSH:
            return f"git@{url}:{name}.git"

        if self is GitProtocol.HTTPS:
            return f"https://{url}/{name}.git"

        raise ClowderError(f"Invalid git protocol")
