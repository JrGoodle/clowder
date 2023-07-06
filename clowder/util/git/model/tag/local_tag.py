"""clowder ref enum

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from clowder.util.console import CONSOLE
from clowder.util.format import Format
# from clowder.util.git.decorators import error_msg
from clowder.util.git.offline import GitOffline

from .tag import Tag


class LocalTag(Tag):
    """Class encapsulating git tag

    :ivar str name: Branch
    :ivar str formatted_ref: Formatted ref
    """

    @property
    def is_checked_out(self) -> bool:
        current_sha = GitOffline.current_head_commit_sha(self.path)
        tag_sha = GitOffline.get_tag_commit_sha(self.path, self.name)
        return current_sha == tag_sha

    @property
    def sha(self) -> str:
        """Commit sha"""
        return GitOffline.get_tag_commit_sha(self.path, self.name)

    def create(self) -> None:
        if self.exists:
            CONSOLE.stdout(f' - Local tag {Format.Git.ref(self.name)} already exists')
            return
        raise NotImplementedError

    # @error_msg('Failed to delete local tag')
    def delete(self) -> None:
        if not self.exists:
            CONSOLE.stdout(f" - Local tag {Format.Git.ref(self.short_ref)} doesn't exist")
            return
        CONSOLE.stdout(f' - Delete local tag {Format.Git.ref(self.short_ref)}')
        GitOffline.delete_local_tag(self.path, name=self.name)

    @property
    def exists(self) -> bool:
        from clowder.util.git.model.factory import GitFactory
        return GitFactory.has_local_tag(self.path, self.name)
