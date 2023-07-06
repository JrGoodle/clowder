"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from pathlib import Path
from typing import Optional

from pygoodle.console import CONSOLE
from pygoodle.format import Format
from pygoodle.git.constants import ORIGIN
# from pygoodle.git.decorators import error_msg
from pygoodle.git.offline import GitOffline
from pygoodle.git.online import GitOnline
from pygoodle.git.model.remote import Remote

from .tag import Tag


class RemoteTag(Tag):
    """Class encapsulating git tag

    :ivar Path path: Path to git repo
    :ivar str name: Tag name
    :ivar str formatted_ref: Formatted ref
    """

    def __init__(self, path: Path, name: str, remote: Optional[str] = None):
        """GitRepo __init__

        :param str name: Tag name
        :param Remote remote: Remote
        """

        remote = ORIGIN if remote is None else remote
        super().__init__(path, name)
        self.remote: Remote = Remote(self.path, remote)

    def __eq__(self, other) -> bool:
        if isinstance(other, RemoteTag):
            return super().__eq__(other) and self.remote.name == other.remote.name
        return False

    def __lt__(self, other: 'RemoteTag') -> bool:
        return f'{self.remote.name}/{self.name}' < f'{other.remote.name}/{other.name}'

    @property
    def is_checked_out(self) -> bool:
        current_sha = GitOffline.current_head_commit_sha(self.path)
        tag_sha = GitOnline.get_remote_tag_sha(self.path, self.name)
        return current_sha == tag_sha

    @property
    def sha(self) -> str:
        """Commit sha"""
        return GitOnline.get_remote_tag_sha(self.path, self.name, self.remote.name)

    def create(self) -> None:
        if self.exists:
            CONSOLE.stdout(f' - Remote tag {Format.Git.ref(self.name)} already exists')
            return
        raise NotImplementedError

    # @error_msg('Failed to delete remote tag')
    def delete(self) -> None:
        if not self.exists:
            CONSOLE.stdout(f" - Remote tag {Format.Git.ref(self.short_ref)} doesn't exist")
            return
        CONSOLE.stdout(f' - Delete remote tag {Format.Git.ref(self.short_ref)}')
        GitOnline.delete_remote_tag(self.path, tag=self.name, remote=self.remote.name, force=True)

    @property
    def exists(self) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_remote_tag(self.path, self.name, self.remote.name)

    def exists_online(self, url: str) -> bool:
        from pygoodle.git.model.factory import GitFactory
        return GitFactory.has_remote_tag(self.path, tag=self.name, remote=self.remote.name, url=url)
