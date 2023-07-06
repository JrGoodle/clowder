"""clowder change

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from enum import auto, unique
from pathlib import Path

from pygoodle.enum import AutoLowerName


@unique
class ChangeType(AutoLowerName):
    ADDED = auto()
    MODIFIED = auto()
    DELETED = auto()


class Change:
    """Class encapsulating git diff

    :ivar Path path: Path to git repo
    """

    def __init__(self, path: Path, file_path: Path, change_type: str, old_sha: str, new_sha: str,
                 old_permissions: str, new_permissions: str):
        """Ref __init__

        :param Path path: Path to git repo
        """

        self.path: Path = path
        self.file_path: Path = file_path
        self.old_sha: str = old_sha
        self.new_sha: str = new_sha
        self.old_permissions: str = old_permissions
        self.new_permissions: str = new_permissions
        self.change_type: ChangeType = ChangeType(change_type)

    def __eq__(self, other) -> bool:
        if isinstance(other, Change):
            return self.path == other.path and \
                   self.file_path == other.file_path and \
                   self.change_type == other.change_type
        return False

    def __lt__(self, other: 'Change') -> bool:
        return self.file_path < other.file_path
