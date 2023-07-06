"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.git.log import GIT_LOG
from pygoodle.git.offline import GitOffline


class Ref:
    """Class encapsulating git ref

    :ivar Path path: Path to git repo
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path):
        """Ref __init__

        :param Path path: Path to git repo
        """

        self.path: Path = path

    def __eq__(self, other) -> bool:
        if isinstance(other, Ref):
            return self.path == other.path
        return False

    @property
    def is_branch(self) -> bool:
        return False

    @property
    def is_tag(self) -> bool:
        return False

    @property
    def is_commit(self) -> bool:
        return False

    @property
    def sha(self) -> Optional[str]:
        """Commit sha"""
        raise NotImplementedError

    @property
    def short_ref(self) -> str:
        """Short git ref"""
        raise NotImplementedError

    @property
    def formatted_ref(self) -> str:
        """Formatted git ref"""

        raise NotImplementedError

    @property
    def date(self) -> Optional[datetime]:
        """Formatted git ref"""

        return GitOffline.get_commit_date(self.path, self.sha)

    @staticmethod
    def truncate_ref(ref: str) -> str:
        """Return bare branch, tag, or sha

        :param str ref: Full pathspec or short ref
        :return: Ref with 'refs/heads/' and 'refs/tags/' prefix removed
        """

        git_branch = "refs/heads/"
        git_tag = "refs/tags/"
        if ref.startswith(git_branch):
            length = len(git_branch)
        elif ref.startswith(git_tag):
            length = len(git_tag)
        else:
            length = 0
        return ref[length:]

    @staticmethod
    def check_ref_format(ref: str) -> bool:
        """Check if git ref is correctly formatted

        :param str ref: Git ref
        :return: True, if git ref is a valid format
        """

        return GitOffline.check_ref_format(ref)

    @staticmethod
    def format_git_branch(branch: str) -> str:
        """Returns properly formatted git branch

        :param str branch: Git branch name
        :return: Branch prefixed with 'refs/heads/'
        """

        prefix = "refs/heads/"
        return branch if branch.startswith(prefix) else f"{prefix}{branch}"

    @staticmethod
    def format_git_tag(tag: str) -> str:
        """Returns properly formatted git tag

        :param str tag: Git tag name
        :return: Tag prefixed with 'refs/heads/'
        """

        prefix = "refs/tags/"
        return tag if tag.startswith(prefix) else f"{prefix}{tag}"

    def checkout(self, check: bool = True, track: bool = False) -> None:
        try:
            GitOffline.checkout(self.path, ref=self.short_ref, track=track)
        except Exception:  # noqa
            message = f'Failed to checkout'
            if check:
                GIT_LOG.error(message)
                raise
            CONSOLE.stdout(f' - {message}')
