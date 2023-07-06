"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique

from pygoodle.enum import AutoLowerName, UnknownEnumCaseError


@unique
class Protocol(AutoLowerName):
    SSH = auto()
    HTTPS = auto()

    def format_url(self, url: str, name: str) -> str:
        """Return formatted git url

        :param str url: Repo url
        :param str name: Repo name
        :return: Full git repo url for specified protocol
        :raise UnknownTypeError:
        """

        if self is Protocol.SSH:
            return f"git@{url}:{name}.git"
        elif self is Protocol.HTTPS:
            return f"https://{url}/{name}.git"
        else:
            raise UnknownEnumCaseError('Invalid git protocol')
