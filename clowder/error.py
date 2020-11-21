"""Clowder error

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""


class ClowderError(Exception):
    pass


class ExistingSymlinkError(ClowderError):
    pass


class DuplicateVersionsError(ClowderError):
    pass


class SourcesValidatedError(ClowderError):
    pass


class DefaultVersionError(ClowderError):
    pass


class MissingYamlError(ClowderError):
    pass


class ExistingVersionError(ClowderError):
    pass


class UnknownTypeError(ClowderError):
    pass


class UnknownProjectError(ClowderError):
    pass


class UnknownArgumentError(ClowderError):
    pass


class MissingFileError(ClowderError):
    pass


class DuplicateRemoteError(ClowderError):
    pass


class ProjectNotFoundError(ClowderError):
    pass


class MissingSourceError(ClowderError):
    pass


class ExistingFileError(ClowderError):
    pass


class MissingClowderRepo(ClowderError):
    pass


class MissingClowderGitRepo(ClowderError):
    pass


class UnknownSourceError(ClowderError):
    pass


class InvalidYamlError(ClowderError):
    pass


class NetworkConnectionError(ClowderError):
    pass


class ProjectStatusError(ClowderError):
    pass


class AmbiguousYamlError(ClowderError):
    pass


class DuplicatePathError(ClowderError):
    pass
