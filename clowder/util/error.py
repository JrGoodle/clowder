"""Clowder error

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""


class ClowderError(Exception):
    pass


class AmbiguousYamlError(ClowderError):
    pass


class ClowderGitError(ClowderError):
    pass


class CommandArgumentError(ClowderError):
    pass


class DefaultVersionError(ClowderError):
    pass


class DuplicateRemoteError(ClowderError):
    pass


class DuplicateVersionsError(ClowderError):
    pass


class ExistingFileError(ClowderError):
    pass


class DuplicatePathError(ClowderError):
    pass


class ExistingVersionError(ClowderError):
    pass


class ExistingSymlinkError(ClowderError):
    pass


class MissingClowderGitRepoError(ClowderError):
    pass


class MissingClowderRepoError(ClowderError):
    pass


class MissingFileError(ClowderError):
    pass


class MissingSourceError(ClowderError):
    pass


class ProjectNotFoundError(ClowderError):
    pass


class ProjectStatusError(ClowderError):
    pass


class SourcesValidatedError(ClowderError):
    pass


class UnknownArgumentError(ClowderError):
    pass


class UnknownProjectError(ClowderError):
    pass


class UnknownTypeError(ClowderError):
    pass


class UnknownSourceError(ClowderError):
    pass
