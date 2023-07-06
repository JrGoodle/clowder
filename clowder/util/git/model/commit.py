"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path

from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.git.offline import GitOffline

from .ref import Ref


class Commit(Ref):
    """Class encapsulating git commit

    :ivar Path path: Path to git repo
    :ivar str sha: Git commit sha
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path, sha: str):
        """GitRepo __init__

        :param Path path: Path to git repo
        :param str sha: Full git commit sha
        """

        super().__init__(path)
        self._sha: str = sha
        self.check_ref_format(self.formatted_ref)

    def __eq__(self, other) -> bool:
        if isinstance(other, Commit):
            return super().__eq__(other) and self.path == other.path
        return False

    @property
    def is_commit(self) -> bool:
        return True

    @property
    def sha(self) -> str:
        """Commit sha"""
        return self._sha

    @property
    def short_ref(self) -> str:
        """Short git ref"""

        return self.sha

    @property
    def formatted_ref(self) -> str:
        """Formatted git ref"""

        return self.sha

    def checkout(self, check: bool = True, track: bool = False) -> None:
        current_commit = GitOffline.current_head_commit_sha(self.path)
        # TODO: Should this always check out detached HEAD?
        if current_commit == self.sha and GitOffline.is_detached(self.path):
            CONSOLE.stdout(' - On correct commit')
            return
        CONSOLE.stdout(f' - Checkout commit {Format.Git.ref(self.short_ref)}')
        super().checkout(check=check, track=track)
