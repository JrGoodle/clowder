"""clowder diff

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import List, Tuple

from pygoodle.git.model.change import Change, ChangeType
from pygoodle.util import sorted_tuple


class Diff:
    """Class encapsulating git diff

    :ivar Path path: Path to git repo
    """

    def __init__(self, path: Path, changes: List[Change]):
        """Ref __init__

        :param Path path: Path to git repo
        """

        self.path: Path = path
        self.added: Tuple[Change, ...] = sorted_tuple([d for d in changes if d.change_type == ChangeType.ADDED])
        self.modified: Tuple[Change, ...] = sorted_tuple([d for d in changes if d.change_type == ChangeType.MODIFIED])
        self.deleted: Tuple[Change, ...] = sorted_tuple([d for d in changes if d.change_type == ChangeType.DELETED])

    @property
    def has_changes(self) -> bool:
        changes = [self.added, self.modified, self.deleted]
        return not any([len(c) > 0 for c in changes])

    @property
    def has_added_files(self) -> bool:
        return bool(self.added)

    @property
    def has_modified_files(self) -> bool:
        return bool(self.modified)

    @property
    def has_deleted_files(self) -> bool:
        return bool(self.deleted)
