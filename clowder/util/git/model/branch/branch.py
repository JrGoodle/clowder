"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.git.model.ref import Ref
from pygoodle.git.offline import GitOffline


class Branch(Ref):
    """Class encapsulating git branch

    :ivar Path path: Path to git repo
    :ivar str name: Branch name
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path, name: str):
        """Branch __init__

        :param Path path: Path to git repo
        :param str name: Branch name
        """

        super().__init__(path)
        self.name: str = name
        self.check_ref_format(self.formatted_ref)

    def __eq__(self, other) -> bool:
        if isinstance(other, Branch):
            return super().__eq__(other) and self.name == other.name
        return False

    @property
    def is_checked_out(self) -> bool:
        current_branch = GitOffline.current_branch(self.path)
        return current_branch == self.name

    @property
    def is_branch(self) -> bool:
        return True

    @property
    def is_tracking_branch(self) -> bool:
        return GitOffline.has_tracking_branch(self.path, self.name)

    def delete(self) -> None:
        raise NotImplementedError

    @property
    def sha(self) -> Optional[str]:
        """Commit sha"""
        raise NotImplementedError

    @property
    def short_ref(self) -> str:
        """Short git ref"""

        return self.truncate_ref(self.name)

    @property
    def formatted_ref(self) -> str:
        """Formatted git ref"""

        return self.format_git_branch(self.name)

    def checkout(self, check: bool = True, track: bool = False) -> None:
        current_branch = GitOffline.current_branch(self.path)
        if current_branch == self.name:
            CONSOLE.stdout(f' - Branch {Format.Git.ref(self.short_ref)} already checked out')
            return
        CONSOLE.stdout(f' - Checkout branch {Format.Git.ref(self.short_ref)}')
        super().checkout(check=check, track=track)
